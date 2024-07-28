from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import load_docs,extract_metadata,extract_all_metadata
import pandas as pd

#takes in a dataframe, runs scraper and returns desired dataframe
def run_llm_scraper(df, llm, schema, tags_to_extract):
    urls = df["url"]
    df = extract_all_metadata(urls,llm,schema,tags_to_extract=tags_to_extract)
    df = pd.DataFrame.from_dict(df,orient='columns')
    df['is_student'] = df.is_author_student_journalist | df.is_article_university_collaboration 
    df.rename(columns={"urls":"url", "news_article_author":"author", "is_student_reported":"is_student"})
    return df["url", "author", "is_student"]
