from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import load_docs,extract_metadata,extract_all_metadata

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

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


urls = ['https://vtdigger.org/2024/02/11/anglers-flock-to-lake-elmore-for-free-ice-fishing-day/','https://vtdigger.org/2023/11/12/construction-of-walk-bike-bridge-over-interstate-now-on-for-2024/',
        "https://www.theplainsman.com/article/2024/05/auburn-mens-golf-team-secures-first-national-championship-caps-historic-season","https://cronkitenews.azpbs.org/2024/05/30/coaches-arizona-poor-numbers-youth-sports-participation/"]


tags_to_extract = ['p','span','a','div']

extracted_tags = extract_all_metadata(urls,llm,schema)
