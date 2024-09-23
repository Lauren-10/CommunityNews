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
    urls = df["url"]
    url_list = urls.to_list() 
    extracted_urls = extract_all_metadata(url_list,llm, prompts,schema,tags_to_extract=tags_to_extract)
    thing = pd.DataFrame.from_dict(extracted_urls,orient='columns')
    student_class = thing["is_author_student_journalist"]

    #df = df.rename(columns={"urls":"url", "news_article_author":"author", "is_student_reported":"is_student"})
    final_dict = {"url": url_list,
                  "author": (list(thing["news_article_author"])),
                  "is_student": student_class}
    return pd.DataFrame.from_dict(final_dict)