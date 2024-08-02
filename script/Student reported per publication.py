import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


dataframe = pd.read_csv('CCN_viz2.csv')
dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)

dataframe['non_student_articles'] = dataframe['num_total_articles'] - dataframe['num_student_articles'] 

#truncating string
dataframe['publication'] = dataframe['publication'].apply(lambda x : x[:20])

dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)

#dataframe = dataframe.sort_values(by='num_total_articles', ascending=False)
breakpoint()
#number of barplots to display
dataframe = dataframe[62:77]
# dataframe = dataframe[181:187]
plt.figure()
#whiteboard
fig, ax = plt.subplots()


#creating top and bottom barplot
sns.barplot(x='publication', y='num_student_articles', data=dataframe, ax=ax, color='purple', label='Student Articles')
sns.barplot(x='publication', y='non_student_articles', data=dataframe, ax=ax, color='yellow', label='Non-student Articles', bottom=dataframe['num_student_articles'])

#rotating x-axis
plt.xticks(rotation=70)

#setting lables 
plt.xlabel('Publication')
plt.ylabel('total number of articles')
plt.title('Student Reporting and Non-Reporting per Publication')

#adding legend 
plt.legend()
plt.tight_layout()
plt.show()

