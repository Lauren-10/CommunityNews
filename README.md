# UVM CommunityNews
Faced with the precarious state of local journalism, resources must be devoted to maintaining and strengthening news organizations in vulnerable areas. As of 2023, 432 US counties contain one or zero local news publications, meaning that they are classified as “news deserts”. News/academic partnerships allow student journalists to contribute to local newspapers, supplementing a lack of journalists in small communities. While many news/academic partnerships exist across the US, an exhaustive study on the impact of these partnerships has not yet been conducted. With CommunityNews, we scrape hundreds of local news websites across the US to identify articles written through news/academic partnerships. This study constitutes the first large-scale assessment of the role of news/academic partnerships across the US. We also present a computational methodology to efficiently study news ecosystems at scale. 
In short, CommunityNews is an open-source news acquisition and classification pipeline built to identify articles published to professional news outlets written by university students. Through pulling data from RSS feeds and feeding article content into an LLM, CommunityNews can efficiently pull information on recent articles published to over four hundred publications.
## Extracted information
CommunityNews can collect the following data from individual articles given RSS feeds from publications through utilizing web scraping and classification techniques (column names in SQL tables given in parenthesis):
Name of Publication article was published to (publication)
- Title of Article (article_title)
- Date of Article publication (date)
- Article Url (url)
- Article Author (author)
- University Student Status (is_student)
## Features
- Utilize fragments of the pipeline for news acquisition or classification
- Extraction of recent articles from a collection of over 400 RSS feeds (composed of articles found from the NELA-Local dataset published by Horne et. al. (2022)
- Identify “hotspots” of student reporting across the country
## Dependencies
Check the requirements.txt file for necessary updates to be made and run setup.py to install any dependencies
