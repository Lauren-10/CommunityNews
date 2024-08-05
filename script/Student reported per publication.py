import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
dataframe = pd.read_csv('ratio.csv')


def student_per_publication(dataframe, plot_function):
    dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)

    dataframe['non_student_articles'] = dataframe['num_total_articles'] - dataframe['num_student_articles'] 

    #truncating string
    dataframe['publication'] = dataframe['publication'].apply(lambda x : x[:20])
    
    #number of barplots to display
    dataframe = dataframe
    return plot_function(dataframe)


def student_to_total_sort_ratio(dataframe):
    dataframe = dataframe.sort_values(by='student_to_total_ratio', ascending=False)
    dataframe = dataframe[40:55]
    plt.figure(figsize=(10,6))
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
    plt.title('Student Reporting and Non-Reporting per Publication \n Sorted by Ratio Student Reporting : Non-Student Reporting')

    #adding legend 
    plt.legend()
    plt.tight_layout()
    return plt.show()

def student_to_total_sort_totalarticles(dataframe):
    dataframe = dataframe.sort_values(by='num_total_articles', ascending=False)
    dataframe = dataframe[:20]
    plt.figure()
    #whiteboard
    fig, ax = plt.subplots()
    #creating top and bottom barplot
    sns.barplot(x='publication', y='num_student_articles', data=dataframe, ax=ax, color='purple', label='Student Articles')
    sns.barplot(x='publication', y='non_student_articles', data=dataframe, ax=ax, color='yellow', label='Non-student Articles', bottom=dataframe['num_student_articles'])

    #rotating x-axis
    plt.xticks(rotation=80)

    #setting lables 
    plt.xlabel('Publication')
    plt.ylabel('total number of articles')
    plt.title('Student Reporting and Non-Reporting per Publication Sorted by Total aricles')

    #setting limits
    plt.ylim()

    #adding legend 
    plt.legend()
    plt.tight_layout()
    return plt.show()

student_per_publication(dataframe, student_to_total_sort_ratio)