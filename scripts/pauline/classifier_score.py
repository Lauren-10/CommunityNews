import pandas as pd 
import numpy as np
df_scraper = pd.read_csv('scraper_dataframe.csv')
df_ground_truth = pd.read_csv('ground_truth_df.csv')


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
    TP = sum((g and s) for g,s in zip(ground_truth_classification, scraper_classification))
    FP = sum((not g and s) for g, s in zip(ground_truth_classification, scraper_classification))
    FN = sum((g and not s) for g,s in zip(ground_truth_classification, scraper_classification))
    precision = ((TP) / (FP + TP)) if (FN + FP) > 0 else 0
    recall = ((TP) / (FN + TP)) if (FN + TP ) > 0 else 0 
    standard_deviation = scraper_classification.std()
    print("standard deviation is", standard_deviation)
    return precision, recall  

"""function for f1_score,
calls precision and recall function from above, and assigns values to variables to work with"""

def f1_score(scraper_classification, ground_truth_classification):
     precision, recall = precision_recall(scraper_classification, ground_truth_classification)
     score = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0
     return score 

# score_value = calculate_classifier_score(df_scraper, df_ground_truth, precision_recall)

# #print
# if score_value == calculate_classifier_score(df_scraper, df_ground_truth, f1_score):
#     print(f"the f1 score value is {score_value}")
# else:
#     print(f"precision and recall is {score_value}")
