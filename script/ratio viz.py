import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
dataframe = pd.read_csv('CCN_viz2.csv')

def ratio_plot(dataframe, ratio_function):
    dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)

    #truncating string
    dataframe['publication'] = dataframe['publication'].apply(lambda x : x[:20])

    #number of barplots to display
    modified_dataframe = dataframe[62:72]
    return ratio_function(modified_dataframe)

def ratio_highest_to_lowest(modified_dataframe):
    breakpoint()
    plt.figure()
    
    #whiteboard
    fig, ax = plt.subplots()
    
    #creating barplot with order
    sns.barplot(x='publication', y='student_to_total_ratio', data = modified_dataframe, ax=ax, order=modified_dataframe['publication'], palette="rocket")

    #rotating x-axis
    plt.xticks(rotation=70)
    
    #setting lables 
    plt.xlabel('Publications')
    plt.ylabel('Ratio')
    plt.title('Ratio of Student to Total Articles per Publication Sorted by Highest to Lowest')

    #setting limits
    ax.set_ylim(0,1)
    
    #adding legend 
    plt.legend()
    plt.tight_layout()
    return plt.show()

ratio_plot(dataframe, ratio_highest_to_lowest)