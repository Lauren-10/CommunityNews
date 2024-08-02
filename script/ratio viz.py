import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


dataframe = pd.read_csv('CCN_viz2.csv')
dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)

#truncating string
dataframe['publication'] = dataframe['publication'].apply(lambda x : x[:20])

#number of barplots to display
dataframe = dataframe[62:77]
# dataframe = dataframe[181:187]
plt.figure()
#whiteboard
fig, ax = plt.subplots()

#creating barplot with order
color = sns.color_palette("light:b")
sns.barplot(x='publication', y='student_to_total_ratio', data=dataframe, ax=ax, order=dataframe['publication'], palette="rocket")

#rotating x-axis
plt.xticks(rotation=70)

#setting lables 
plt.xlabel('Publications')
plt.ylabel('Ratio')
plt.title('Ratio of Student to Total Articles per Publication')

#setting limits
ax.set_ylim(0,1)

#adding legend 
plt.legend()
plt.tight_layout()
plt.show()

