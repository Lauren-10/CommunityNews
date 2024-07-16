import pandas as pd
file_location = r'C:\Users\manav\Desktop\community news internship web scraping\CommunityNews\Bylines Project -RSS feeds - Manual entry .csv'
df= pd.read_csv(file_location)
if [df['Is_student_journalist '].notnull()]:
    df_ground_truth = df[['Article Name', 'URL ','Partnership ','Is_student_journalist ']]
print(df_ground_truth.head())