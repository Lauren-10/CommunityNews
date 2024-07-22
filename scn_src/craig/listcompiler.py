import pandas as pd
with open('pub_feed.csv') as file:
    lines = [line.strip() for line in file]
    pubs = []
    urls = []
    for line in lines:
        ele = line.split(',')
        pubs.append(ele[0])
        urls.append(ele[1])
    for pub in pubs:
        pubs[pubs.index(pub)] = pub.lower().replace(' ','')
    pubs = pd.Series(pubs, name='publication')
    urls = pd.Series(urls, name='feed')
    my_rss = pd.concat([pubs,urls], axis=1)
    nela = pd.read_csv('NELA_list.csv')
    masterlist = pd.concat([my_rss,nela]).drop_duplicates(keep=False)
    masterlist.to_csv('RSS_masterlist.csv', index=False)


