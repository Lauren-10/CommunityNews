from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import load_docs,extract_metadata,extract_all_metadata
import pandas as pd

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


urls = ["https://voiceofoc.org/2024/07/orange-countys-push-for-its-first-veterans-cemetery-gains-momentum/",
"https://voiceofoc.org/2024/07/orange-countys-push-for-its-first-veterans-cemetery-gains-momentum/"]


tags_to_extract = ['p','span','a','div']

df = extract_all_metadata(urls,llm,schema,tags_to_extract=tags_to_extract)
pd.DataFrame.from_dict(df,orient='columns')
#df = extracted_tags.rename(columns={df.columns[0]: "title", df.columns[1]: "author_name", df.columns[2]: "is_author_student"})
#print(df['url'])
pprint.pprint(df)
list1 = [x for x in df x[0]['is_author_student_journalist']]
df = pd.DataFrame([{'is_author_student_journalist':list1, 'urls':urls}])
df.insert(0, "urls", urls)
df.insert(1, 'news_article_title', 1)
df.insert(2, 'news_article_author', 2)
df.insert(3, 'is_author_student_journalist', 3)
df.insert(4, 'is_article_university_collaboration', 4)
df.to_csv("test_data.csv")
print(df.head())


