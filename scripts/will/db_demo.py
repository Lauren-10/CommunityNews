from scn_src.db_connectors import MySQLConnector
import pandas as pd 
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

df = pd.DataFrame([{'Name': 'Will', 'Age': 22, 'Major': 'Computer Science', 'GPA': 3.5},{ 'Name': 'John', 'Age': 21, 'Major': 'Math', 'GPA': 3.0}])

df = pd.DataFrame([{'Name': 'Billy', 'Age': 22, 'Major': 'Computer Science', 'GPA': 3.5},{ 'Name': 'John', 'Age': 21, 'Major': 'Math', 'GPA': 3.0}])


#instantiate the connectors
db_reader = MySQLConnector('wthomps3',permission = 'reader')#this is the connector that will be used to read from the database
db_admin = MySQLConnector('wthomps3',permission = 'admin')#this is the connector that will be used to write to the database

db_admin.load_data_to_sql('users',df,if_exists = 'replace')

db_reader.query_db("SELECT * FROM users")







