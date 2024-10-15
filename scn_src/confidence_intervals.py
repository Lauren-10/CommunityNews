import pandas as pd 
import numpy as np
from .llm_scraper_function import run_llm_scraper

#function for percision and recall
def precision_recall(scraper_classification, ground_truth_classification):
    """
    called by auto_precision_recall. compares is_student results from scraper and hand-annotated dataset,
    calculates precision and recall scores based on frequency of true positives, false positives, and false negatives

    Parameters:
    scraper_classification(list(bool)): contains is_student values for the ChatGPT scraper
    ground_truth_classification(list(bool)): contains is_student values for the hand_annotated dataset

    Returns:
    floats: precision, recall, and f1 diagnostics
    """
    TP = sum((g and s) for g,s in zip(ground_truth_classification, scraper_classification))
    FP = sum((not g and s) for g, s in zip(ground_truth_classification, scraper_classification))
    FN = sum((g and not s) for g,s in zip(ground_truth_classification, scraper_classification))
    precision = ((TP) / (FP + TP)) if (TP + FP) > 0 else 0 
    recall = ((TP) / (FN + TP)) if (FN + TP ) > 0 else 0 
    f1_score = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0 

    return precision, recall, f1_score



def confidence_interval_precision(precision_values):
    '''
    creates an array of precision scores and calculates mean and 95% confidence interval
    
    Parameter: 
    precision_values (list(float)): precision scores in sample
    
    Returns: float
    '''

    data_array = np.array(precision_values)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1)  #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_precision = stats.t.interval(confidence_level, degrees_freedom, loc=sample_mean, scale=standard_error)
    print(f"Sample Mean Precision: {sample_mean}")
    print(f"95% Confidence Interval Precision: {confidence_interval_precision}")
    return confidence_interval_precision


def confidence_interval_recall(recall_values):
    '''
    creates an array of recall scores and calculates mean and 95% confidence interval
    
    Parameter: 
    recall_values (list(float)): recall scores in sample
    
    Returns: float
    '''
    data_array = np.array(recall_values)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1) #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_recall = stats.t.interval(confidence_level, degrees_freedom, loc=sample_mean, scale=standard_error)
    print(f"Sample Mean Recall: {sample_mean}")
    print(f"95% Confidence Interval Recall: {confidence_interval_recall}")
    return confidence_interval_recall

#confidence interval for f1
#sample array, outputs for f1
def confidence_interval_f1(f1_values):
    '''
    creates an array of f1 scores and calculates mean and 95% confidence interval
    
    Parameter: 
    f1_values (list(float)): f1 scores in sample
    
    Returns: float
    '''
    
    data_array = np.array(f1_values)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1) #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    confidence_interval_f1 = stats.t.interval(confidence_level, degrees_freedom, loc=sample_mean, scale=standard_error)
    print(f"Sample Mean F1: {sample_mean}")
    print(f"95% Confidence Interval F1: {confidence_interval_f1}")
    return confidence_interval_f1


def auto_precision_recall(num_chunks, llm, prompts, schema, tags_to_extract, ground_truth_csv):
    '''
    calculates the 95% confidence interval for a sample of precision, recall, 
    and f1_scores based on ChatGPT's performance in identifying students.

    num_chunks (int): specifies the number of times diagnostics are calculated
    llm (ChatOpenAI class object): specifies temperature and model name
    prompts (list of strs): defined in prompt_draft.py
    schema (Article(BaseModel) class object): specifies structure of llm output
    tags_to_extract (list of strs): locates portions of HTML for scraper to process
    ground_truth_df (str): directory pathway to ground truth csv

    Returns:
    dict

    '''
    #create empty lists for each diagnostic
    precision_values = []
    recall_values = []
    f1_values = []



    #load hand-annotated dataset to which ChatGPT will compare its peformance
    df_ground_truth = pd.read_csv(ground_truth_csv)

    #run ChatGPT on the same dataset a specified number of times
    df_scraper = run_llm_scraper(df_ground_truth, llm=llm, prompts=prompts, schema=schema, tags_to_extract=tags_to_extract)
    for _ in range(num_chunks):
        df_ground_truth_sample = df_ground_truth.sample(df_ground_truth.shape[0], replace=True)
        df_scraper_sample = df_scraper.iloc[df_ground_truth_sample.index.values]
        precision, recall, score = precision_recall(list(df_scraper_sample["is_student"]) , list(df_ground_truth_sample["is_student_reported"]))
        precision_values.append(precision)
        recall_values.append(recall)
        f1_values.append(score)

    #calculate the mean and 95% confidence interval for each diagonstic
    precision_confidence = confidence_interval_precision(precision_values)
    recall_confidence = confidence_interval_recall(recall_values)
    f1_confidence = confidence_interval_f1(f1_values)
    return {"precision confidence": precision_confidence,
            "recall confidence": recall_confidence,
            "f1 confidence": f1_confidence}