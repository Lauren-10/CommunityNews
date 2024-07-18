from scn_src.db_connectors import MySQLConnector
from scn_src.functions import create_blank_table
import pandas as pd 
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import random

db_admin = MySQLConnector('wthomps3', permission = 'admin') #this is the connector that will be used to write to the database

webscraper_df = pd.DataFrame({"publication":["fakepub"], "url":["fakeurl"], "article_title":["faketitle"], "date":["2024-01-01"] })
chatgpt_df = pd.DataFrame({"url":["fakeurl"], "author":["fakeauthor"], "is_student":[random.randint(0,1)]})


create_blank_table(db_admin, "student_journalists23_24_test")

# #STEP 1: grab feeds from SQL as a df
query = '''
    SELECT *
    FROM `rss_masterlist`
'''
feeds_df = db_admin.load_df_from_table(query)

# #STEP 2: scrape each RSS feed, create publication/url/title/date df
unnamed_scraper_function(feeds_df)
# #produce df variable "webscraper_data_df"

# #STEP 3: append df to SQL table
db_admin.add_df_to_table("webscraper_data", webscraper_data_df)

# #STEP 4: ChatGPT each url in "webscraper_data_df", create url/author/is_student df
unnamed_gpt_function(webscrape_data_df)
# #produce df variable "chatgpt_data_df"

# #STEP 5: append df to SQL table
db_admin.add_df_to_table("chatgpt_data", chatgpt_data)

# #STEP 6: join tables 
join_query = '''
    SELECT publication, webscraper_test.url, article_title, date, author, is_student
    FROM webscraper_test
    JOIN chatgpt_test ON webscraper_test.url = chatgpt_test.url;'''

final_table = db_admin.load_df_from_table(join_query)

db_admin.add_df_to_table("student_journalists23_24_test", final_table)
