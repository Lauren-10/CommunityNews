from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import pandas as pd

def parse_url(txtfile):
    rss = []
    news_sources = []
    title = []
    date = []
    #dates2 = []
    with open(txtfile) as file: 
        lines = [line.strip() for line in file]
        for line in lines:
            x = line.split(",")
            link = rss_url(x[1])
            rss.append(link[0])
            title.append(link[1])
            date.append(link[2])
            news_sources.append(x[0])


    df = pd.DataFrame({"name_of_news_source": news_sources,
                       "list_of_urls" : rss,
                       "title" : title,
                       "date_of_pub" : date})
    df = df.explode(["list_of_urls", "title", "date_of_pub"])
    df = df.reset_index(drop = True)
   
    df.to_csv("urls.csv")



def rss_url(link):
    xml_links = []
    titles = []
    dates = []
    page = urlopen(link)
    xml_bytes = page.read()
    xml = xml_bytes.decode("utf-8")
    rss_u = BeautifulSoup(xml, features="xml")
    xml_links = rss_u.find_all("link")
    titles = rss_u.find_all("title")
    date = rss_u.find_all("pubDate")
    xml_links.pop(0)
    xml_links.pop(0)
    titles.remove(titles[0])
    links = []
    title = []
    pub_date =[]
    for i in xml_links:
        links.append(i.text)
        title.append(titles[xml_links.index(i)].text)
        pub_date.append(date[xml_links.index(i)].text)
    titles2 = title[:10]
    return [links, titles2, pub_date]

if __name__ == "__main__":
    parse_url("rssfeeds.txt")