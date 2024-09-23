from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from langchain_community.document_loaders import AsyncChromiumLoader
import xml.etree.ElementTree as ET
import html
import tqdm


"""
Function load_rss_feed takes a list of urls and finds all items
"""
def load_rss_feed(urls, file):

    if file == False:
        loader = AsyncChromiumLoader(urls)
        docs = loader.load()
        decoded_content = html.unescape(docs[0].page_content)
        bs = BeautifulSoup(decoded_content, "lxml-xml")
        return bs.find_all("item")
    else:
        #add a way to work with files here
        print("files don't work yet!")



"""
Add specific try and except blocks
"""

"""
parse_url takes a data frame filled with news sources
and their rss feeds and writes to another csv article titles,
date published, author name, and the news source it originated from
"""
#convert input to data frame
#df_rss: pd.DataFrame
def parse_url(df_rss: pd.DataFrame):
    #empty lists to store data from scraping
    rss = []
    news_sources = []
    title = []
    date = []
    test_dates = []

    #lines 41-44 convert the dataframe to a csv
    #to run the code with a casv, comment out the lines
    df_rss.to_csv("rss_urls.csv")

    #open file of rss information
    with open("rss_urls.csv") as file: 

        #get all lines of the file into a list 
        #iterate over the list to call rss_url function
        lines = [line.strip() for line in file]
        lines.pop(0)
    
        for line in tqdm.tqdm(lines):
            
            #handles key error from rss_url function
            
            #split line of text into news source and rss link
            x = line.split(",")
            #call rss_url function 
            link = rss_url(x[1], x[2])
            
            if link == {}:
                continue

            #Verify date and append text accordingly
            try:
                test_dates = link["Publication Date"]
            except TypeError:
                continue

            #counter for indexing purposes
            i = 0
            for pub_date in test_dates:
                    
                #use regex to identify and pull year
                test_date = re.findall(r"20\d{2}", pub_date)[0]
                #pull data that was only published in 2024 or 2023, bypass all else
                if test_date == "2024" or test_date == "2023":
                    date.append(datetime.strptime(pub_date[0:16], "%a, %d %b %Y"))
                    #date.append(pub_date)
                    news_sources.append(link["News Station"][i])
                    rss.append(link["Links"][i])
                    title.append(link["Titles"][i])
                    i = i + 1
                else:
                    i = 0
                    continue

    #Write this dataframe as a list of dictionaries instead of multiple lists
    df = pd.DataFrame({"publication": news_sources,
                       "url" : rss,
                       "article_title" : title,
                       "date" : date,
                       "author": ["null" for i in range(len(news_sources))],
                       "is_student": ["null" for i in range(len(news_sources))]})
    df = df.explode(["publication","url", "article_title", "date"])
    df = df.reset_index(drop = True)

    #dataframe return
    return df
    
    #csv return
    #df.to_csv("urls.csv")



def rss_url(news_source, link):  
    #handling the various exceptions (403, formating, etc.)
    #initializing lists for data collection
    titles = []
    links = []
    pub_date = []

    #open link to rss feed
    items = load_rss_feed([link], False)

    #return none if no item tags exist in the rss feed
    if len(items) == 0:
        return None
    

    #Pull anything with an item tag and find the information
    #contained within each item tag
    try:
        for item in items:
            titles.append(item.find("title").text.strip())
            links.append(item.find("link").text.strip())
            pub_date.append(item.find("pubDate").text.strip()) 
    except AttributeError:
        return {}

    #return dictionary of article information for one news source
    return {"News Station" : [news_source for i in range(len(links))],
            "Links": links,
            "Titles" : titles,
            "Publication Date": pub_date} 
        
