from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import load_docs,extract_metadata,extract_all_metadata
import pandas as pd
df_ground_truth = pd.read_csv('ground_truth_df.csv')
url = df_ground_truth['urls'].values
print(url)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Transform

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_author": {"type": "string"},
        "news_article_publication_date": {"type": "string"},
        "is_author_student_college_student": {"type":"boolean"},
        "is_author_student_journalist": {"type":"boolean"},
        "is_article_university_collaboration": {"type":"boolean"}
    },
    "required": ["news_article_title","news_article_summary", "news_article_author",'is_author_student_journalist','is_article_university_collaboration','is_author_college_student'],
}

urls = url

tags_to_extract = ['p','span','a','div']

df = extract_all_metadata(urls,llm,schema,tags_to_extract=tags_to_extract)
breakpoint()
df = pd.DataFrame.from_dict(df,orient='columns')
pprint.pprint(df)
print(type(df))
print(df.columns)
df['is_student_reported'] = df.is_author_student_journalist | df.is_article_university_collaboration 
print(df.columns)
df.to_csv('scraper_dataframe.csv')