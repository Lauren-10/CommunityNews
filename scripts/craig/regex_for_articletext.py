import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

#Step 1, input csv containing urls -> pandas ->  beautiful soups
df = pd.read_csv("urls.csv")
article_text = []
list = []
urls = df.list_of_urls
for url in urls:
    article = ""
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    #Step 2, beautiful soup to text body
    paragraphs = soup.find_all("p")
    for i in paragraphs:
        article = article + i.text
    article_text.append(article)
    list.append(url)

#Step 3, search text body with regex input
true_or_false = []
for x in article_text:
    email = re.search("([A-Z]*[a-z]*[0-9]*[._-]*)@smail\\.astate\\.edu", x)
    if email != None:
        true_or_false.append(True)
    else:
        true_or_false.append(False)
student_reporter = pd.DataFrame({'urls': list, 'student_reporter': true_or_false})
print(student_reporter)