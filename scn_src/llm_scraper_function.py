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
def run_llm_scraper(df, llm, prompts, schema, tags_to_extract):
    #breakpoint()
    urls = df["url"]
    url_list = urls.to_list() #craig-added line
    #print(f'urls:{urls}')
    extracted_urls = extract_all_metadata(url_list,llm, prompts,schema,tags_to_extract=tags_to_extract)
    thing = pd.DataFrame.from_dict(extracted_urls,orient='columns')
    df = thing.rename(columns={"urls":"url", "news_article_author":"author", "is_author_student_journalist":"is_student"})

    return df
