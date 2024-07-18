#takes the two dfs and merges them and calculates precision, recall and f1
import pandas as pd 
df_scraper = pd.read_csv('scraper_dataframe.csv')
df_ground_truth = pd.read_csv('ground_truth_df.csv')
#function that merges the dataframe and returns score function with bolean values 
def calculate_classifier_score(df_scraper, df_ground_truth, score_function):
    merged_dataframe = pd.merge(df_ground_truth, df_scraper[['is_student_reported', 'urls']], on='urls', how='left', suffixes=('_ground_truth', '_scraper'))
    scraper_classification = merged_dataframe['is_student_reported_scraper']
    ground_truth_classification = merged_dataframe['is_student_reported_ground_truth']
    #print(scraper_classification)
    #print(ground_truth_classification)
    return score_function(scraper_classification, ground_truth_classification)

#function for percision what parameters does it take? 
def precision_recall(scraper_classification, ground_truth_classification):
    TP = (scraper_classification == True) & (ground_truth_classification == True).sum()
    FP = ((scraper_classification == True)) & (ground_truth_classification == False).sum()
    FN = ((scraper_classification == True)) & (ground_truth_classification == False).sum()
    TN = ((scraper_classification == False)) & (ground_truth_classification == False).sum()
    print(TP)
    precision = ((TP) / (FP + TP)) if (FN + FP).values[0] > 0 else 0
    recall = ((TP) / (FN + TP)) if (FN + TP ).values[0] > 0 else 0 
    return precision, recall  

#function for f1_score 
def f1_score(scraper_classification, ground_truth_classification):
     precision, recall = precision_recall(scraper_classification, ground_truth_classification)
     score = (precision * recall) / (precision + recall)
     return score 

#print(df_scraper.columns)
#print(df_ground_truth.columns)
score_value = calculate_classifier_score(df_scraper, df_ground_truth, precision_recall)
#print(score_value)