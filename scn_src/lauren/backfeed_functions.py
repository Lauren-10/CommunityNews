import os
from urllib.parse import quote

"""
Plan of attack:
1: 
- Load the urls as the xml documents they are
- establish a path for each documents
- place these paths into a glob object
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
    xml_doc_encode = quote(xml_doc, safe='')
    #assert isinstance(xml_doc,str)
    print(xml_doc_encode)
    #Pull doc and retrieve items (element tree?)

    #establish file path


if __name__ == "__main__":
    backfeed_loader(100, "https://zunews.com/feed/")