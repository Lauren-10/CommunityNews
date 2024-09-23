from scn_src.db_connectors import MySQLConnector
from scn_src.rss_to_html import parse_url
from scn_src.llm_scraper_function import run_llm_scraper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from langchain_openai import ChatOpenAI
from multiprocessing import Pool
import pandas as pd 
import numpy as np
import glob as gb
import os
from functools import partial

#count the number of cpu's. 
#Comment 15 for single processing, and comment 16 for multiprocessing.
#num_cpus = os.cpu_count()
num_cpus = 1

#The connector that will be used to write to the database
db_admin = MySQLConnector('wthomps3', permission = 'admin')

#input feeds, a df containing every RSS feed
'''perhaps adjust this function to contain the .csv to df step'''
#scrape each RSS feed, create df of publication/url/title/date and NULL columns author/is_student, add to database
def backfeed_to_sql(feeds,table_name='student_journalists23_24'): 
    df = parse_url(feeds)
    db_admin.add_df_to_table(table_name, df, if_exists='replace')

#inner loop for the scraper, called with multiprocessing.pool
def scraper_inner_loop(df,llm,schema,prompt,tags_to_extract,table_name):
    db_admin = MySQLConnector('wthomps3', permission = 'admin')
    chatgpt_data_df = run_llm_scraper(df, llm, prompt,schema, tags_to_extract)

    #remove apostrophes from author names
    chatgpt_data_df.author = chatgpt_data_df.author.str.replace(r"[\"\']","")
    
    #update each row in sql
    with db_admin.engine.connect() as connection:
        for i,row in chatgpt_data_df.iterrows():
            sql_query = f"UPDATE {table_name} SET author = '{row['author']}', is_student = {row['is_student']} WHERE url = '{row['url']}'"
            connection.execute(text(sql_query))
        connection.commit()
        
#create n-row chunks of student_journalists23_24 and append them to a list
def chatgpt_to_sql(df,chunk_size,llm,prompts,schema,tags_to_extract,table_name = 'student_journalists23_24v2'):
    if df.shape[0]%chunk_size != 0:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0]-chunk_size, chunk_size)]
        list_df.append(df[:-df.shape[0]%chunk_size])
    else:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0], chunk_size)]

    scraper_inner_loop_partial = partial(scraper_inner_loop,llm=llm,schema=schema,prompt=prompt,tags_to_extract=tags_to_extract,table_name=table_name,)

    #Toggle
    #go through each chunk w/o multiprocessing
    for df in list_df:
        scraper_inner_loop(df,llm,schema,prompts,tags_to_extract,table_name)

    #go through each chunk WITH multiprocessing
    #with  Pool(num_cpus) as pool: 
        #pool.map(scraper_inner_loop_partial,list_df)

#call this function to start querying the llm in chunks of specified size
def outer_chatgpt_to_sql(chunk_size,llm,schema,prompts,tags_to_extract,table_name = 'student_journalists23_24v2'):
    df = db_admin.load_df_from_table(f'SELECT * FROM {table_name} WHERE is_student IS NULL')
    df = df.sample(frac = 1).reset_index(drop = True)# stop the same webstie form being queried multiple times in a row to avoid IP bans
    chatgpt_to_sql(df,chunk_size,llm,prompts,schema,tags_to_extract,table_name)