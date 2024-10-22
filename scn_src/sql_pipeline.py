from scn_src.rss_to_html import parse_url
from scn_src.llm_scraper_function import run_llm_scraper
from sqlalchemy.sql import text
from multiprocessing import Pool
import pandas as pd 
import os
from functools import partial

def feeds_to_sql(db_admin, rss_feed_csv, table_name):
    '''
    Sends finalized rss feed list to MySQL.

    Parameters:
    db_admin(MySQLConnector class object): MySQL user CRAIG CHECK IF THIS IS SUCCINCT ENOUGH
    rss_feeds_csv(str): file pathway to .csv containing RSS feeds for each publication
    table_name(str): name of MySQL table to be created/updated

    Returns: none
'''
    try:
        # Open and read the file
        with open(rss_feed_csv) as file:
            df = pd.read_csv(file)
            #send dataframe to sql
            db_admin.add_df_to_table(table_name, df)     

    except Exception as e:
        print(f"An error occurred: {e}")

def urls_to_sql(db_admin, feeds_table, final_table): 
    '''
    Runs parse_url on all feeds in the datafram and updates specified MySQL table with 
    publication, is_uni_newspaper, url, article_title, and date columns filled. author and is_student fields will remain NULL.

    Parameters:
    db_admin(MySQLConnector class object): specifies MySQL client username and permission level
    feeds_table (str): the name of the MySQL table created by feeds_to_MySQL
    table_name (str): the name of the MySQL table to be updated/created

    Returns: none
'''
    query = f"""
    SELECT *
    FROM {feeds_table}
    """

    feeds_df = db_admin.load_df_from_table(query)
    final_df = parse_url(feeds_df)
    db_admin.add_df_to_table(final_table, final_df, if_exists='replace')

    #replace 'null' string with NULL
    with db_admin.engine.connect() as connection:
        for i,row in final_df.iterrows():
            sql_query = f"UPDATE {final_table} SET author = NULL, is_student = NULL WHERE author = 'null'"
            connection.execute(text(sql_query))
        connection.commit()
    print(f"added data to {final_table} in MySQL")


def scraper_inner_loop(df, llm, prompts, schema, tags_to_extract, table_name, db_admin):
    '''
    Called by chatgpt_to_sql. Runs run_llm_scraper on each chunk, 
    then updates the author and is_student columns in indicated MySQL table.
    
    Parameters:
    df (df): a chunk created in the last step
    llm (ChatOpenAI class object): specifies temperature and model name
    prompts (list of strs): defined in prompt_draft.py
    schema (Article(BaseModel) class object): specifies structure of llm output
    tags_to_extract (list of strs): locates portions of HTML for scraper to process
    table_name (str): the name of the MySQL table to be updated with author and is_student columns
    db_admin(MySQLConnector class object): specifies MySQL client username and permission level

    Returns: none
'''
    chatgpt_data_df = run_llm_scraper(df=df, llm=llm, prompts=prompts, schema=schema, tags_to_extract=tags_to_extract)
    chatgpt_data_df.news_article_author = chatgpt_data_df.news_article_author.str.replace(r"[\"\']","") #remove apostrophes from author names

    #update each row in sql
    with db_admin.engine.connect() as connection:
        for i,row in chatgpt_data_df.iterrows():
            sql_query = f"UPDATE {table_name} SET author = '{row['news_article_author']}', is_student = {row['is_author_student_journalist']} WHERE url = '{row['urls']}'"
            connection.execute(text(sql_query))
        connection.commit()
    print(f'added data to {table_name} in MySQL')
    

def chatgpt_to_sql(chunk_size, llm, prompts, schema, tags_to_extract, table_name, db_admin, multiprocessor_on):
    '''
    Selects portion of MySQL table in which ChatGPT data has not yet entered, separates rows into chunks of specified size, 
    and runs scraper_inner_loop on each.

    Parameters:
    chunk_size (int): specifies the number of urls processed at a time
    llm (ChatOpenAI class object): specifies temperature and model name
    prompts (list of strs): defined in prompt_draft.py
    schema (Article(BaseModel) class object): specifies structure of llm output
    tags_to_extract (list of strs): locates portions of HTML for scraper to process
    table_name (str): the name of the MySQL table to be updated with author and is_student columns
    db_admin(MySQLConnector class object): specifies MySQL client username and permission level
    multiprocessor_on (bool): toggles multiprocessing capability for multiple cpu's

    Returns: none
'''
    df = db_admin.load_df_from_table(f'SELECT * FROM {table_name} WHERE is_student IS NULL')
    df = df.sample(frac = 1).reset_index(drop = True)# stop the same webstie form being queried multiple times in a row to avoid IP bans
    
    if df.shape[0]%chunk_size != 0:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0]-chunk_size, chunk_size)]
        list_df.append(df[:-df.shape[0]%chunk_size])
    else:
        list_df = [df[i:i+chunk_size] for i in range(0,df.shape[0], chunk_size)]
    
    scraper_inner_loop_partial = partial(scraper_inner_loop,llm=llm,prompts=prompts,schema=schema,tags_to_extract=tags_to_extract,db_admin=db_admin,table_name=table_name,)

    if multiprocessor_on == False:
        for chunk in list_df:
            scraper_inner_loop(chunk, llm=llm, prompts=prompts, schema=schema, tags_to_extract=tags_to_extract, db_admin=db_admin, table_name=table_name)
    elif multiprocessor_on == True:
        num_cpus = os.cpu_count()
        with  Pool(num_cpus) as pool: 
            pool.map(scraper_inner_loop_partial, list_df)


"""
example arguments:

db_admin = MySQLConnector('wthomps3', permission = 'admin')
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
tags_to_extract = ['p','span','a','div']
table_name = 'example_table'
schema = Article
"""