import pandas as pd 
import numpy as np
from spicy import stats
df_ground_truth = pd.read_csv('ground_truth_df.csv')
from classifier_score import precision_recall
from classifier_score import f1_score
from langchain_openai import ChatOpenAI
from llm_scraper_function import run_llm_scraper

def auto_precision_recall(num_chunks, llm, schema):
    print("hello")
    precision_values = []
    recall_values = []
    df_ground_truth = pd.read_csv('ground_truth_df.csv')
    df_ground_truth = df_ground_truth.iloc[0].reset_index()
    breakpoint()
    df_scraper = run_llm_scraper(df_ground_truth["urls"], llm, schema)
    for _ in range(num_chunks):
        precision, recall = precision_recall(df_scraper, df_ground_truth)
        precision_values = float(precision)
        precision_values.append(precision)
        recall_values =float(recall)
        recall_values.append(recall)
    f1_values = []
    for _ in range (num_chunks):
        f1 = f1_score(df_scraper, df_ground_truth)
        f1_values = float(f1)
        f1_values.append(f1)
    precision_confidence = confidence_interval_precision(precision_values)
    recall_confidence = confidence_interval_recall(recall_values)
    f1_confidence = confidence_interval_f1(f1_values)
    return {"precision confidence": precision_confidence,
            "recall confidence": recall_confidence,
            "f1 confidence": f1_confidence}




#confidence interval for precision
#sample array, outputs for precision
def confidence_interval_precision(precision_values):
    data_precision = [precision_values]
    data_array = np.array(data_precision)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1)  #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_precision = stats.t.interval(confidence_level, degrees_freedom, sample_mean, standard_error)
    print(f"Sample Mean: {sample_mean}")
    print(f"95% Confidence Interval Precision: {confidence_interval_precision}")
    return confidence_interval_precision

#confidence interval for recall
#sample array, outputs for recall
def confidence_interval_recall(recall_values):
    data_recall = [recall_values]
    data_array = np.array(data_recall)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1) #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_recall = stats.t.interval(confidence_level, degrees_freedom, sample_mean, standard_error)
    print(f"Sample Mean: {sample_mean}")
    print(f"95% Confidence Interval: {confidence_interval_recall}")
    return confidence_interval_recall

#confidence interval for f1
#sample array, outputs for f1
def confidence_interval_f1(f1_values):
    data_f1 = [f1_values]
    data_array = np.array(data_f1)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1) #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_recall = stats.t.interval(confidence_level, degrees_freedom, sample_mean, standard_error)
    print(f"Sample Mean: {sample_mean}")
    print(f"95% Confidence Interval: {confidence_interval_f1}")
    return confidence_interval_f1


if __name__ =="__main__":
    print("start")
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    schema = {
        "properties": {
            "news_article_title": {"type": "string"},
            "news_article_author": {"type": "string"},
            "news_article_publication_date": {"type": "string"},
            "is_author_student_college_student": {"type":"boolean"},
            "is_author_student_journalist": {"type":"boolean"},
            "is_article_university_collaboration": {"type":"boolean"}
        },
        "required": ["news_article_title","news_article_summary", "news_article_author",'is_author_student_journalist','is_article_university_collaboration','is_author_college_student'],
    }
    tags_to_extract = ['p','span','a','div']
    print(auto_precision_recall(3, llm, schema, tags_to_extract))