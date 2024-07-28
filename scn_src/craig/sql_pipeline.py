from scn_src.db_connectors import MySQLConnector
from scn_src.lauren.rss_to_html import parse_url
from scn_src.functions import create_blank_table
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
num_cps = os.cpu_count()

db_admin = MySQLConnector('wthomps3', permission = 'admin') #this is the connector that will be used to write to the database
#arguments for ChatGPT portion
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



def big_function1(feeds,table_name='student_journalists23_24'):
    #STEP 2: scrape each RSS feed, create publication/url/title/date df
    df = parse_url(feeds)
    """DELETE WHEN LAUREN UPDATES webscraper_data_df TO CONTAIN NULL ROWS FOR author AND is_student_journalist"""

    # #STEP 3: append df to SQL table
    db_admin.add_df_to_table(table_name, df, if_exists='replace')
    
    
def outer_big_function2(chunk_size,llm,schema,table_name = 'student_journalists23_24'):
    #query the TABLE_NAME table and select all values where is_student is null and return these as a df 
    #df = db_admin.table_to_df(SELECT * FROM student_journalist23_24 WHERE 'is_student'=NULL)
    #big_function2(df,....)
    pass

def big_function2(df,chunk_size,llm,schema,table_name = 'student_journalists23_24'):
    list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0],chunk_size)]
    list_df.append(df[:-df.shape[0]%chunk_size])
    
    def scraper_inner_loop(df,llm,schema,tags_to_extract,table_name):
        #inner loop for the scraper, called with multiprocessing.pool
        chatgpt_data_df = run_llm_scraper(df, llm, schema, tags_to_extract)
        sql_query = f"UPDATE {table_name} SET 'author` = %s, 'is_student' = %s WHERE 'url'=%s"
        with db_admin.engine.connect() as connection:
            for i,row in chatgpt_data_df.iterrows():
                connection.execute(text(sql_query)),(row['author'],row['is_student'],row['url'])
            connection.commit() 
                
    scraper_inner_loop_partial = partial(scraper_inner_loop,llm=llm,schema=schema,tags_to_extract=tags_to_extract,table_name=table_name)
    
    with  Pool(num_cps) as pool: 
        pool.map(scraper_inner_loop_partial,list_df)
        
        #STEP 4: ChatGPT each chunk in "webscraper_data_df", create url/author/is_student df
        chatgpt_data_df = run_llm_scraper(df, llm, schema, tags_to_extract)
    

        # #STEP 5: append df to SQL table
        # db_admin.add_df_to_table("chatgpt_data", chatgpt_data_df)

    #STEP 6: join tables 
    join_query = '''
        SELECT publication, is_uni_newspaper, webscraper_test.url, article_title, date, author, is_student
        FROM webscraper_test
        JOIN chatgpt_test ON webscraper_test.url = chatgpt_test.url;'''

    final_table = db_admin.load_df_from_table(join_query)

    db_admin.add_df_to_table("student_journalists23_24", final_table)
    
    
