# import pandas as pd
# with open('pub_feed.csv') as file:
#     lines = [line.strip() for line in file]
#     pubs = []
#     urls = []
#     for line in lines:
#         ele = line.split(',')
#         pubs.append(ele[0])
#         urls.append(ele[1])
#     for pub in pubs:
#         pubs[pubs.index(pub)] = pub.lower().replace(' ','')
#     pubs = pd.Series(pubs, name='publication')
#     urls = pd.Series(urls, name='feed')
#     my_rss = pd.concat([pubs,urls], axis=1)
#     nela = pd.read_csv('NELA_list.csv')
#     masterlist = pd.concat([my_rss,nela]).drop_duplicates(keep=False)
#     masterlist.to_csv('RSS_masterlist.csv', index=False)


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
df0 = pd.read_csv('urls_7.csv')



# df1 = df0[:500]
# df2 = df0[500:1000]
# df3 = df0[1000:1500]
# df4 = df0[1500:2000]
# df5 = df0[2000:2500]
# df6 = df0[2500:3000]
# df7 = df0[3000:3500]
# df8 = df0[3500:]

db_admin.add_df_to_table('webscraper_data', df0)