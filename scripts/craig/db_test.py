from scn_src.db_connectors import MySQLConnector
from scn_src.functions import create_blank_table
import pandas as pd 
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import random

db_admin = MySQLConnector('wthomps3',permission = 'admin')#this is the connector that will be used to write to the database

df = pd.DataFrame({"url":["FAKEURL1","FAKEURL2"], "publication":["FAKEPUB1","FAKEPUB2"], "article_title":["FAKETITLE1","FAKETITLE2"], "date":["2013-01-01","2013-01-02"], "author":["",""], "is_student_journalist":["",""]})
query = '''
    SELECT *
    FROM `url_list`
'''

db_admin.load_data_to_sql("url_list", df)
#load data from sql to df
urls = db_admin.load_df_from_table(query)

#for each in row, apply chatgpt to get 0/1, update sql with Author and Is_student
#ASK PAULINE HOW AUTHOR
# tf = pd.Series([random.randint(0,1)])
# author = pd.Series(["Craig Rettew"])

# def hack_gpt(dataframe, tf_metadata, author_metadata):
#     for row in df:
#         df['is_student_journalist'] = tf[row]
#         df.author = "Craig Rettew"
#     return df

# hack_gpt(urls,tf,author)