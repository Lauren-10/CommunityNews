import pandas as pd
file_location = r'C:\Users\manav\Desktop\community news internship web scraping\CommunityNews\Bylines Project -RSS feeds - Manual entry .csv'
df= pd.read_csv(file_location)
df = df[df['Is_student_journalist '].notnull()]
df_ground_truth = df[['Article Name', 'Partnership ','Is_student_journalist ', 'URL ']]
print(df_ground_truth.head())
df_ground_truth = df_ground_truth.rename(columns={'Article Name' : 'news_article_title', 'URL ' : 'urls', 'Partnership' : 'partnership', 'Is_student_journalist ' : 'is_student_reported'})                            
df_ground_truth.to_csv('ground_truth_df.csv')

