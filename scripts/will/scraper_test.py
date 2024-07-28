
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup
from langchain_community.document_transformers import Html2TextTransformer


#import asyncio
#from playwright.async_api import async_playwright
#
#async def scrape_rss():
#    # Start Playwright in an asynchronous context
#    async with async_playwright() as p:
#        # Launch a browser; headless can be set to False to see the browser UI
#        browser = await p.chromium.launch(headless=True)
#        # Create a new page
#        page = await browser.new_page()
#
#        # URL of the RSS feed
#        url = 'https://vtdigger.org/feed'
#        breakpoint()
#        print()
#        # Navigate to the URL
#        await page.goto(url)
#
#        # Assuming links in the RSS are within <link> tags directly in the feed XML
#        # Fetch all link elements; adjust the selector as necessary
#        links = await page.query_selector_all('link')
#
#        content = await page.content()
#        print(content)
#
#        # Extract and print each link URL
#        for link in links:
#            # Get the text content of each link element
#            link_url = await link.text_content()
#            print(link_url)
#
#        # Close the browser
#        await browser.close()
#
## Run the asynchronous function
#
#
#
#
#result = asyncio.run(scrape_rss())
import html
urls = ["https://vtdigger.org/feed"]
def load_rss_feed(urls):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    decoded_content = html.unescape(docs[0].page_content)
    bs = BeautifulSoup(decoded_content, 'lxml-xml')
    bs.find_all("link")


#print(docs_transformed)


#from selenium import webdriver
#from bs4 import BeautifulSoup
#import pandas as pd
#import html
#import datetime
#
#
#def initialize_driver():
#    options = webdriver.ChromeOptions()
#    options.add_argument('--headless=new')
#    options.add_argument('--disable-gpu')
#    options.add_argument('--no-sandbox')
#
#    return webdriver.Chrome(options=options)
#
#
#def get_product_data(driver, url):
#    driver.get(url)
#    content = driver.page_source
#    soup = BeautifulSoup(content, features="html.parser")
#    return soup
#
#driver = initialize_driver()
#a = get_product_data(driver, 'https://vtdigger.org/feed')
#
#
#
#from selenium.webdriver.firefox.options import Options
#from selenium import webdriver
#
#import os
#foxprofiledir = os.path.expanduser("~/.mozilla/firefox/<i>random-string</i>.selenium")
#
#options = options()
#options.headless = true
#
#driver = webdriver.firefox(firefox_profile=foxprofiledir, options=options)
#driver = webdriver.firefox()    # a browser window pops up
#driver.get("https://vtdigger.org/feed")
#fullhtml = driver.page_source
#
#from selenium import webdriver
#from selenium.webdriver.chrome.service import service
#from selenium.webdriver.chrome.options import options
#
## set up chrome options
#chrome_options = options()
#chrome_options.add_argument("--headless")  # run chrome in headless mode
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#
## Specify the path to the ChromeDriver if not in PATH
#chromedriver_path = "/path/to/chromedriver"
#
## Set up the WebDriver service
#service = Service(chromedriver_path)
#
## Create the WebDriver instance
#driver = webdriver.Chrome(service=service, options=chrome_options)
#
## Example usage
#driver.get("https://www.example.com")
#print(driver.title)
#
## Close the driver
#driver.quit()
#
#
#
#
#
#
##$urls = ["https://vtdigger.org/feed"]
##$loader = AsyncChromiumLoader(urls)
##$docs = loader.load()
##$#doc = loader.load()[0].page_content
##$
##$#docs = loader.load()
##$print(docs[0])
##$transformer = BeautifulSoupTransformer()
##$doc = transformer.transform_documents(docs,tags_to_extract = ['link'])
##$#
##$
##$#html2text = Html2TextTransformer()
##$#docs_transformed = html2text.transform_documents(docs)
##$
##$print(doc)
##$
##$#bs = BeautifulSoup()
##$#bs_doc = bs(doc,'html.parser')
##$#
#$#str_a = "Hello World"
#$#
#def say(my_str):
#    print(my_str)


