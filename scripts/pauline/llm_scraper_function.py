import pandas as pd
from pauline_file_copy import extract_all_metadata

#takes in a dataframe, runs scraper and returns desired dataframe
def run_llm_scraper(df, llm, schema, tags_to_extract):
    urls = df["url"]
    url_list = urls.to_list() #craig-added line
    #print(f'urls:{urls}')
    extracted_urls = extract_all_metadata(url_list,llm,schema,tags_to_extract=tags_to_extract)
    thing = pd.DataFrame.from_dict(extracted_urls,orient='columns')
    #print(f'thing: {thing}')
    student_class = []
    for i in range(df.shape[0]):
        student_class.append(thing["is_author_student_journalist"][i] | thing["is_article_university_collaboration"][i])
    #df = df.rename(columns={"urls":"url", "news_article_author":"author", "is_student_reported":"is_student"})
    final_dict = {"url": url_list,
                  "author": thing["news_article_author"],
                  "is_student": student_class}
    print(f"final dict: {final_dict}")
    return pd.DataFrame.from_dict(final_dict)