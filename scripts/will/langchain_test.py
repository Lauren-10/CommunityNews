#from langchain_community.document_loaders import AsyncHtmlLoader
#from langchain_community.document_transformers import BeautifulSoupTransformer
#from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import AsyncChromiumLoader
#from langchain.chains import create_extraction_chain
#import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import extract, scrape_with_playwright,load_docs

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Transform

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_author": {"type": "string"},
        "news_article_publication_date": {"type": "string"},
    },
    "required": ["news_article_title","news_article_summary", "news_article_author"],
}


urls = ["https://www.nytimes.com/2019/06/20/technology/tech-giants-antitrust-law.html","https://vtcynic.com/features/its-more-than-a-drunk-cig-cigarettes-on-uvms-campus/","https://www.sevendaysvt.com/news/scott-vetoes-renewable-energy-bill-40969930"]

docs = load_docs(urls)
extracted_content_list()

for doc in docs: 
        extracted_content = extract(schema=schema, content=doc,llm = llm)
        extracted_content_list.append(extracted_content)
