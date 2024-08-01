from scn_src.db_connectors import MySQLConnector
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import pandas as pd

db_admin = MySQLConnector('wthomps3', permission = 'admin')

# COMBINED TABLE
'''SELECT s.publication, r.is_uni_newspaper, s.url, s.article_title, s.date, s.author, s.is_student
FROM student_journalists23_24 s
JOIN rss_masterlist r USING (publication)'''

#number of student articles per publication
'''
WITH combined_table AS (
    SELECT s.publication, r.is_uni_newspaper, s.url, s.article_title, s.date, s.author, s.is_student
    FROM student_journalists23_24 s
    JOIN rss_masterlist r USING (publication))
SELECT publication, COUNT(1) AS NumStuArticles
FROM combined_table
WHERE is_student = 1 AND is_uni_newspaper = 0
'''

#Number of total articles per publication/date vs student ones,
'''
WITH combined_table AS (
    SELECT
        s.publication,
        r.is_uni_newspaper,
        s.url,
        s.article_title,
        s.date,
        s.author,
        s.is_student
    FROM
        student_journalists23_24 s
    JOIN
        rss_masterlist r
    USING (publication)
)SELECT
    date,
    is_uni_newspaper,
    SUM(is_student) as student_articles,
	COUNT(is_student) as total_articles
FROM
    combined_table
GROUP BY
    date
'''

#articles per author
'''
WITH combined_table AS(
    SELECT s.publication, r.is_uni_newspaper, s.url, s.article_title, s.date, s.author, s.is_student
    FROM student_journalists23_24 s
    JOIN rss_masterlist r USING (publication))
SELECT
	author,
    COUNT(1) AS num_articles
FROM
	combined_table
GROUP BY
	author
ORDER BY
	num_articles DESC;
'''
combined_table_query = """SELECT s.publication, r.is_uni_newspaper, s.url, s.article_title, s.date, s.author, s.is_student
    FROM student_journalists23_24 s
    JOIN rss_masterlist r USING (publication)"""


#find duplicate urls
"""
SELECT
    url, COUNT(url)
FROM
    student_journalists23_24
GROUP BY
    url
HAVING
    COUNT(url) > 1
"""

#for pickups, find duplicate headlines
'''
SELECT
    article_title, COUNT(article_title)
FROM
    student_journalists23_24
GROUP BY
    article_title
HAVING
    COUNT(article_title) > 1
'''


#charts
#data_viz1: student and non-student reporting by day
data_viz1_query = """
WITH combined_table AS (
    SELECT
        s.publication,
        r.is_uni_newspaper,
        s.url,
        s.article_title,
        s.date,
        s.author,
        s.is_student
    FROM
        student_journalists23_24 s
    JOIN
        rss_masterlist r
    USING (publication)
)SELECT
    date,
    SUM(is_student) as student_articles,
	COUNT(is_student) as total_articles
FROM
    combined_table
WHERE
	is_uni_newspaper = false
GROUP BY
    date
ORDER BY
    date
"""
#data_viz2: which publications have the highest ratio of student reports/total reports?
data_viz2_query = """
WITH joined_table AS (
    SELECT
        s.publication,
        r.is_uni_newspaper,
        s.url,
        s.article_title,
        s.date,
        s.author,
        s.is_student
    FROM
        student_journalists23_24 s
    JOIN
        rss_masterlist r
    USING (publication)
)SELECT
    publication,
    SUM(is_student) as num_student_articles,
	COUNT(is_student) as num_total_articles,
    ROUND(SUM(is_student) / COUNT(is_student), 3) AS student_to_total_ratio
FROM
    joined_table
GROUP BY
    publication
ORDER BY
	student_to_total_ratio DESC;
"""
data_viz2_df = db_admin.load_df_from_table(data_viz2_query)
data_viz2_df.fillna(value= int(0), inplace= True)
data_viz2_df.to_csv("data_viz2.csv", index=False)