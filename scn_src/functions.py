import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from scn_src.db_connectors import MySQLConnector

#create a blank table
def create_blank_table(connector, table_name):
    create_table = f'''CREATE TABLE IF NOT EXISTS {table_name} (
    publication varchar(255),
    url varchar(255),
    article_title varchar(255),
    date DATE,
    author varchar(255),
    is_student tinyint(1))
    '''
    connector.query_db(create_table)
    print("table created")

#given PROPERLY LABELED df's of URLS and REGEX, print a df showing whether or not each url was student-written
def scan_with_regex(url_df, regex_df):
    article_text = []
    list = []
    url_list = url_df["list_of_urls"]
    for url in url_list:
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
    # #Step 3, search text body with regex input
    regex_cols = regex_df["regex"]
    true_or_false = []
    for x in article_text:
        for regex in regex_cols:
            t_or_f = False
            match = re.search(regex, x)
            if match != None:
                t_or_f = True
                break
        true_or_false.append(t_or_f)
                
    student_reporter = pd.DataFrame({'urls': list, 'student_reporter': true_or_false})
    print(student_reporter)