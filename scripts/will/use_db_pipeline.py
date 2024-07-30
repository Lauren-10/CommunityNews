from scn_src.db_connectors import MySQLConnector
from scn_src.craig.rss_to_html_copy import parse_url
from scn_src.llm_scraper_function import run_llm_scraper
from scn_src.db_connectors import MySQLConnector
from scn_src.craig.rss_to_html_copy import parse_url
from scn_src.llm_scraper_function import run_llm_scraper
from scn_src.sql_pipeline import outer_chatgpt_to_sql,backfeed_to_sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from langchain_openai import ChatOpenAI

if __name__ == "__main__":    
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



    #df = db_admin.load_df_from_table("SELECT * FROM rss_masterlist")
    #backfeed_to_sql(df)
    outer_chatgpt_to_sql(5,llm,schema,tags_to_extract)

    

