from scn_src.db_connectors import MySQLConnector
from scn_src.lauren.rss_to_html import parse_url
from scn_src.functions import create_blank_table
from scn_src.llm_scraper_function import run_llm_scraper
import pandas as pd 
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from langchain_openai import ChatOpenAI

db_admin = MySQLConnector('wthomps3', permission = 'admin') #this is the connector that will be used to write to the database

# arguments for ChatGPT portion
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
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

# #STEP 1: grab feeds from SQL as a df
query = '''
    SELECT *
    FROM `rss_masterlist`
'''
feeds_df = db_admin.load_df_from_table(query)

# #STEP 2: scrape each RSS feed, create publication/url/title/date df
webscraper_data_df = parse_url(feeds_df)

# #STEP 3: append df to SQL table
db_admin.add_df_to_table("webscraper_data", webscraper_data_df)

# #STEP 4: ChatGPT each url in "webscraper_data_df", create url/author/is_student df
chatgpt_data_df = run_llm_scraper(webscraper_data_df, llm, schema, tags_to_extract)
# #produce df variable "chatgpt_data_df"

# #STEP 5: append df to SQL table
db_admin.add_df_to_table("chatgpt_data", chatgpt_data_df)

# #STEP 6: join tables 
join_query = '''
    SELECT publication, is_uni_newspaper, webscraper_test.url, article_title, date, author, is_student
    FROM webscraper_test
    JOIN chatgpt_test ON webscraper_test.url = chatgpt_test.url;'''

final_table = db_admin.load_df_from_table(join_query)

db_admin.add_df_to_table("student_journalists23_24", final_table)

