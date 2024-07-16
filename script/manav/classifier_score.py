import pandas as pd 
#function that merges the dataframe and returns score function with bolean values 
def calculate_classifier_score(df_scraper, df_ground_truth, score_function):
    merged_dataframe = pd.merge(df_ground_truth, df_scraper[['Is_student_reported']], on='urls', how='left')
    scraper_classification = merged_dataframe['is_student_reported_scraper']
    ground_truth_classification = merged_dataframe['is_student_reported_ground_truth']
    return score_function(scraper_classification, ground_truth_classification)

#function for percision what parameters does it take? 
def precision_recall(scraper_classification, ground_truth_classification):
    TP = ((scraper_classification == True) & (ground_truth_classification == True)).sum()
    FP = ((scraper_classification == True)) & (ground_truth_classification == False).sum()
    FN = ((scraper_classification == True)) & (ground_truth_classification == False).sum()
    TN = ((scraper_classification == False)) & (ground_truth_classification == False).sum()
    precision = (TP / (FN + TP)) if (FN + FP) > 0 else 0
    recall = (TP / (FN + TP)) if (FN + TP ) > 0 else 0 
    return precision, recall  

#function for f1_score 
def f1_score(scraper_classification, ground_truth_classification):
     precision, recall = percision_recall(scraper_classification, ground_truth_classification)
     score = (precision * recall) / (precision + recall)
     return score 

