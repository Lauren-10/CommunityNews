import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
dataframe = pd.read_csv('timeline.csv')

#modify the dataframe to plot according to dates
def timeline_plot(dataframe, plot_function):
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    dataframe['month_and_year'] = dataframe['date'].dt.strftime("%m/%Y")
    dataframe = dataframe.groupby('month_and_year', sort = False).count()
    return plot_function(dataframe)

def timeline_barplot(dataframe):
    plt.figure()
    #whiteboard
    fig, ax = plt.subplots()

    #creating top and bottom barplot
    sns.barplot(x='month_and_year', y='student_articles', data=dataframe, ax=ax, color='purple', label='Student-Reporting')
    sns.barplot(x='month_and_year', y='non_student articles', data=dataframe, ax=ax, color='yellow', label='NonStudent-Reporting', bottom=dataframe['student_articles'])

    #rotating x-axis
    plt.xticks(rotation=45)

    #setting lables 
    plt.xlabel('Date')
    plt.ylabel('Number of Reporting')
    plt.title('Student Reporting and Non-Reporting Timeline')

    #setting week limits 
    # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

    #adding legend 
    plt.legend()
    plt.tight_layout()

    return plt.show()

timeline_plot(dataframe, timeline_barplot)