from scn_src.db_connectors import MySQLConnector
import pandas as pd 
import numpy as np

#push a datafame to a table in the database
def push_df_to_sql(df,table_name,connector):
    connector.load_data_to_sql(table_name,df)
    return df

df = pd.DataFrame({'Name': 'Will', 'Age': 22, 'Major': 'Computer Science', 'GPA': 3.5})





