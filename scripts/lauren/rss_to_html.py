from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from langchain_community.document_loaders import AsyncChromiumLoader
import xml.etree.ElementTree as ET
import html

"""
Function load_rss_feed takes a list of urls and finds all items
"""
def load_rss_feed(urls):
    try:
        loader = AsyncChromiumLoader(urls)
        docs = loader.load()
        decoded_content = html.unescape(docs[0].page_content)
        bs = BeautifulSoup(decoded_content, "lxml-xml")
        return bs.find_all("item")
        #add a way to work with xml files
    except:
        return []



"""
parse_url takes a data frame filled with news sources
and their rss feeds and writes to another csv article titles,
date published, author name, and the news source it originated from
"""
#convert input to data frame
def parse_url(df_rss: pd.DataFrame):
    #empty lists to store data from scraping
    rss = []
    news_sources = []
    title = []
    date = []
    test_dates = []

    df_rss.to_csv("rss_urls.csv")
 
    #open file of rss information
    with open("rss_urls.csv") as file: 

        #get all lines of the file into a list 
        #iterate over the list to call rss_url function
        lines = [line.strip() for line in file]
        lines.pop(0)

        for line in lines:

            #handles key error from rss_url function
            try:
                #split line of text into news source and rss link
                x = line.split(",")

                #call rss_url function 
                link = rss_url(x[1], x[2])

                #Verify date and append text accordingly
                test_dates = link["Publication Date"]

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
            except:
                continue

    #Write this dataframe as a list of dictionaries instead of multiple lists
    df = pd.DataFrame({"name_of_news_source": news_sources,
                       "list_of_urls" : rss,
                       "title" : title,
                       "date_of_pub" : date})
    df = df.explode(["name_of_news_source","list_of_urls", "title", "date_of_pub"])
    df = df.reset_index(drop = True)
   
    df.to_csv("urls.csv")



def rss_url(news_source, link):  
    #handling the various exceptions (403, formating, etc.)
    #initializing lists for data collection
    titles = []
    links = []
    pub_date = []

    #open link to rss feed
    items = load_rss_feed([link])

    #return none if no item tags exist in the rss feed
    if len(items) == 0:
        return None
    

    #Pull anything with an item tag and find the information
    #contained within each item tag
    for item in items:
        titles.append(item.find("title").text.strip())
        links.append(item.find("link").text.strip())
        pub_date.append(item.find("pubDate").text.strip())  

    #return dictionary of article information for one news source
    return {"News Station" : [news_source for i in range(len(links))],
            "Links": links,
            "Titles" : titles,
            "Publication Date": pub_date} 
        

if __name__ == "__main__":
    data = [["thehornettribune" , "https://asuhornettribune.com/feed/"], ["wvua23", "https://www.wvua23.com/feed/"], ["deltadigitalnewsservice" , "https://deltanewsservice.com/feed/"], ["KNKX", "https://www.knkx.org/news.rss"]]
    df = pd.DataFrame(data)
    parse_url(df)