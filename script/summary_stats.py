import pandas as pd 
dataframe = pd.read_csv('combined_table.csv')
dataframe = dataframe[dataframe['is_student'].notnull()]
is_student = dataframe.loc[dataframe.is_student == 1]
not_student = dataframe.loc[dataframe.is_student == 0]
print(not_student)

# qeueries

""" 1. calculate number of news articles per publication 

WITH journalists AS
	(
    SELECT * FROM `student_journalists23_24` 
	WHERE (is_student) = 1
     )
SELECT *,
	SUM(is_student) OVER 
        (
       	PARTITION BY publication
        ROWS BETWEEN UNBOUNDED PRECEEDING AND UNBOUNDED FOLLOWING
        ) AS avg_articles_per_publication
        FROM journalists """

""" 2. """