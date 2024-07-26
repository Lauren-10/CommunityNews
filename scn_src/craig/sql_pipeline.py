from scn_src.db_connectors import MySQLConnector
from rss_to_html_copy import parse_url
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

#count the number of cpu's 
num_cpus = os.cpu_count()

#this is the connector that will be used to write to the database
db_admin = MySQLConnector('wthomps3', permission = 'admin')

#default arguments for ChatGPT portion
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
schema = {
    "properties": {
        "news_article_author": {"type": "string"},
        "is_author_student_college_student": {"type":"boolean"},
        "is_author_student_journalist": {"type":"boolean"},
        "is_article_university_collaboration": {"type":"boolean"}
    },
    "required": ["news_article_author",'is_author_student_journalist','is_article_university_collaboration','is_author_college_student'],
}
tags_to_extract = ['p','span','a','div']

#input feeds, a df containing every RSS feed
#scrape each RSS feed, create df of publication/url/title/date and NULL columns author/is_student, add to database
def backfeed_to_sql(feeds,table_name='student_journalists23_24'): 
    df = parse_url(feeds)
    db_admin.add_df_to_table(table_name, df, if_exists='replace')
    #db_admin.load_data_to_sql(table_name, df)

#inner loop for the scraper, called with multiprocessing.pool
def scraper_inner_loop(df,schema,tags_to_extract,table_name, llm=None):
    db_admin = MySQLConnector('wthomps3', permission = 'admin')
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chatgpt_data_df = run_llm_scraper(df, llm, schema, tags_to_extract)
    with db_admin.engine.connect() as connection:
        for i,row in chatgpt_data_df.iterrows():
            sql_query = f"UPDATE {table_name} SET author = '{row['author']}', is_student = {row['is_student']} WHERE url = '{row['url']}'"
            connection.execute(text(sql_query))
        connection.commit()
        
#create n-row chunks of student_journalists23_24 and append them to a list
def chatgpt_to_sql(df,chunk_size,llm,schema,tags_to_extract,table_name = 'student_journalists23_24'):
    if df.shape[0]%chunk_size != 0:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0]-chunk_size, chunk_size)]
        list_df.append(df[:-df.shape[0]%chunk_size])
    else:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0], chunk_size)]

    scraper_inner_loop_partial = partial(scraper_inner_loop,schema=schema,tags_to_extract=tags_to_extract,table_name=table_name)
    #scraper_inner_loop_partial = partial(scraper_inner_loop,llm=llm,schema=schema,tags_to_extract=tags_to_extract,table_name=table_name)
    with  Pool(num_cpus) as pool: 
        pool.map(scraper_inner_loop_partial,list_df)
    
def outer_chatgpt_to_sql(chunk_size,llm,schema,tags_to_extract,table_name = 'student_journalists23_24'): 
    df = db_admin.load_df_from_table(f'SELECT * FROM {table_name} WHERE is_student IS NULL')
    chatgpt_to_sql(df,chunk_size,llm,schema,tags_to_extract,table_name)
    pass

outer_chatgpt_to_sql(2,llm,schema,tags_to_extract,table_name='sj_test')