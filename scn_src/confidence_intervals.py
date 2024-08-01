import pandas as pd 
import numpy as np
from spicy import stats
from .llm_scraper_function import run_llm_scraper


#function that merges the dataframe and returns score function with boolean values 
def calculate_classifier_score(df_scraper, df_ground_truth, score_function):
    merged_dataframe = pd.merge(df_scraper, df_ground_truth[['is_student_reported', 'urls']], on='urls', how='left', suffixes=('_scraper', '_ground_truth'))
    ground_truth_classification = merged_dataframe['is_student_reported_ground_truth']
    scraper_classification = merged_dataframe['is_student_reported_scraper']
    return score_function(scraper_classification, ground_truth_classification)

#function for percision and recall
def precision_recall(scraper_classification, ground_truth_classification):
    """takes in two dataframes, zips it and each boolean from the zip corresponds to g and s respectively 
    g and s is true if both g,s = true, true
    not g and s is true if g,s = false, true 
    g and not s is true if g,s = true, false"""
    print(f"ground_truth_classification: {ground_truth_classification}")
    print(f"scraper_classification: {scraper_classification}")
    TP = sum((g and s) for g,s in zip(ground_truth_classification, scraper_classification))
    FP = sum((not g and s) for g, s in zip(ground_truth_classification, scraper_classification))
    FN = sum((g and not s) for g,s in zip(ground_truth_classification, scraper_classification))
    precision = ((TP) / (FP + TP)) if (TP + FP) > 0 else 0 #FN
    recall = ((TP) / (FN + TP)) if (FN + TP ) > 0 else 0 
    #standard_deviation = scraper_classification.std()
   # print("standard deviation is", standard_deviation)
    return precision, recall  


"""function for f1_score,
calls precision and recall function from above, and assigns values to variables to work with"""

def f1_score(scraper_classification, ground_truth_classification):
     precision, recall = precision_recall(list(scraper_classification["is_student"]), (list(ground_truth_classification["is_student_reported"])))
     score = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0
     return score 

# score_value = calculate_classifier_score(df_scraper, df_ground_truth, precision_recall)

# #print
# if score_value == calculate_classifier_score(df_scraper, df_ground_truth, f1_score):
#     print(f"the f1 score value is {score_value}")
# else:
#     print(f"precision and recall is {score_value}")


#confidence interval for precision
#sample array, outputs for precision
def confidence_interval_precision(precision_values):
    #data_precision = [precision_values]
    data_array = np.array(precision_values)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1)  #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    breakpoint()
    confidence_interval_precision = stats.t.interval(confidence_level, degrees_freedom, loc=sample_mean, scale=standard_error)
    print(f"Sample Mean Precision: {sample_mean}")
    print(f"95% Confidence Interval Precision: {confidence_interval_precision}")
    return confidence_interval_precision

#confidence interval for recall
#sample array, outputs for recall
def confidence_interval_recall(recall_values):
    #data_recall = [recall_values]
    data_array = np.array(recall_values)
    sample_mean = np.mean(data_array)
    sample_std = np.std(data_array, ddof=1) #ddof = 1 signifies it is a sample vs entire population
    n = len(data_array)
    standard_error = sample_std / np.sqrt(n)
    confidence_level = 0.95
    degrees_freedom = n - 1
    breakpoint()
    confidence_interval_recall = stats.t.interval(confidence_level, degrees_freedom, loc=sample_mean, scale=standard_error)
    print(f"Sample Mean Recall: {sample_mean}")
    print(f"95% Confidence Interval Recall: {confidence_interval_recall}")
    return confidence_interval_recall

#confidence interval for f1
#sample array, outputs for f1
def confidence_interval_f1(f1_values):
    #data_f1 = [f1_values]
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


def auto_precision_recall(num_chunks, llm, prompts, schema, tags_to_extract):
    precision_values = []
    recall_values = []
    df_ground_truth = pd.read_csv('ground_truth_df.csv')
    df_ground_truth = df_ground_truth.sample(10)
    #df_ground_truth = df_ground_truth.iloc[0:1].reset_index()
    breakpoint()
    df_scraper = run_llm_scraper(df_ground_truth, llm, prompts, schema, tags_to_extract)
    for _ in range(num_chunks):
        precision, recall = precision_recall(list(df_scraper["is_student"]) , list(df_ground_truth["is_student_reported"]))
        precision_values.append(precision)
        recall_values.append(recall)
    f1_values = []
    for _ in range (num_chunks):
        f1 = f1_score(df_scraper, df_ground_truth)
        f1_values.append(f1)
    breakpoint()
    precision_confidence = confidence_interval_precision(precision_values)
    recall_confidence = confidence_interval_recall(recall_values)
    f1_confidence = confidence_interval_f1(f1_values)
    return {"precision confidence": precision_confidence,
            "recall confidence": recall_confidence,
            "f1 confidence": f1_confidence}