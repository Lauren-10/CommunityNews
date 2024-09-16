import os
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
"""
Notes:
run the command "source ~/.bashrc" before 
using this function
it makes everyone's lives easier
including my own
"""

"""
The asyncronous function backfeed_loader
takes the number of snapshots wanted and the rss_feed
returns an XML document containing larger history of articles
"""
def backfeed_loader(num_snaps: int, rss_feed: str):
    #Set needed variables
    #Retrieve Backfeed key from environment
    BACKFEED_API_KEY = os.environ.get("BACKFEED_API_KEY")

    #URL Format: https://backfeed.app/KEY/OPTIONS/URL
    xml_doc = f"https://backfeed.app/{BACKFEED_API_KEY}/s:{num_snaps}/{rss_feed}"

    response = requests.get(xml_doc)
    soup = BeautifulSoup(response.content, features="xml")
    
    #Pull doc and retrieve items (element tree?)
    #make document name
    doc_name = rss_feed.split("/")[2].split(".")[0] + ".xml"
    doc_path = "backfeed_files"
    file_path = os.path.join(doc_path, doc_name) 
    with open(file_path, 'w') as f:
        f.write(soup.prettify())
    #establish file path



if __name__ == "__main__":
    backfeed_loader(5, "https://zunews.com/feed/")