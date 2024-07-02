from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import pandas as pd

def parse_url(txtfile):
    rss = []
    news_sources = []
    with open(txtfile) as file: 
        lines = [line.strip() for line in file]
        print(lines)
        for line in lines:
            x = line.split(",")
            rss.append(rss_url(x[1]))
            news_sources.append(x[0])
    df = pd.DataFrame({"name of news source": news_sources,
                       "list of rss feeds" : rss})
    df.to_csv("urls.csv")



def rss_url(link):
    xml_links = []
    lst = []
    page = urlopen(link)
    xml_bytes = page.read()
    xml = xml_bytes.decode("utf-8")
    rss_u = BeautifulSoup(xml, features="xml")
    xml_links = rss_u.find_all("link")
    links = []
    for i in xml_links:
        links.append(i.text)
    for i in links:
        try:
            page = urlopen(i)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            lst.append(BeautifulSoup(html, "html.parser"))
        except:
            continue
    return lst

if __name__ == "__main__":
    print(type(rss_url("https://www.andalusiastarnews.com/rss")[0]))