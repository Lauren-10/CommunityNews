#from langchain_community.document_loaders import AsyncHtmlLoader
#from langchain_community.document_transformers import BeautifulSoupTransformer
#from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import AsyncChromiumLoader
#from langchain.chains import create_extraction_chain
#import pprint
from langchain_openai import ChatOpenAI
from scn_src.lang_chain_utils import extract, scrape_with_playwright

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Transform

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_author": {"type": "string"},
        "news_article_publication_date": {"type": "string"},
    },
    "required": ["news_article_title","news_article_summary", "news_article_author"],
}


urls = ["https://www.theplainsman.com/article/2024/06/we-will-not-go-at-auburns-pace-university-employees-unionize-for-living-wage", 
        "https://deltanewsservice.com/2024/05/31/legends-bbq-a-thriving-figure-of-the-nea-black-community/", 
        "https://cronkite.asu.edu/experiences/cronkite-news-phoenix/", 
        "https://eldonnews.org/top-stories/2024/05/29/slushcult-is-a-community-built-on-nostalgia/", 
        "https://oaklandnorth.net/2024/06/24/oakland-mayor-thao-fbi-raid-this-wouldnt-have-gone-down-the-way-it-did-if-i-was-rich/", 
        "https://richmondconfidential.org/2024/07/06/richmond-art-center-view-from-here-art-exhibit-offers-prisoners-perspective/", 
        "https://xtown.la/2024/06/25/more-street-racing-and-sideshows-in-los-angeles-but-few-effective-laws/", 
        "https://www.uscannenbergmedia.com/2024/07/06/barbie-laments-everything-respects-nothing/",  
        "https://hunewsservice.com/local/dispensaries-open-using-legal-loopholes/",
        "https://www.theplainsman.com/article/2024/05/auburn-mens-golf-team-secures-first-national-championship-caps-historic-season",
        "https://www.wvua23.com/take-a-look-at-tuscaloosas-newest-attraction-popstroke-minigolf/",
        "https://zunews.com/2024/04/issues-with-commuting-and-off-campus-housing/"]

extracted_content = scrape_with_playwright(urls, schema=schema,llm = llm)
