import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.option_context('display.max_columns', None, 'display.max_rows', None)

def make_total_medal_column(df, column_name, column_list):

    df[column_name] = df[column_list].sum(axis=1)
    df.sort_values(by=[column_name], ascending=False,inplace=True)

    return df

def convert_to_numeric(df):

    column_list = list(df)
    for e in column_list:
        medal_count = df[e].str.replace(',','')
        medal_count = pd.to_numeric(medal_count)
        df[e] = medal_count

    return df

def read_csv_files(file1, file2):

    summer_df = pd.read_csv('Olympics_dataset1.csv', thousands=',')
    winter_df = pd.read_csv('Olympics_dataset2.csv',thousands=',')
    
    return summer_df, winter_df

def join_and_clean_tables(summer_df, winter_df):

    summer_df = summer_df.drop(axis=0,index=0)
    total_df = pd.merge(summer_df, winter_df, how='left', on=['Team'])
    total_df = total_df.drop(total_df.columns[12:], axis=1)
    total_df.columns = ['Country', 'summer_rubbish', 'summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze', 'summer_total', 'winter_participation', 'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total']
    
    return total_df
    
def question_1(print_val):

    summer_df, winter_df = read_csv_files('Olympics_dataset1.csv','Olympics_dataset2.csv')
    q1_df = join_and_clean_tables(summer_df, winter_df)
    q1_df = q1_df[q1_df.Country != 'Totals']
    #q1_df.to_csv('q1.csv')
    if print_val:
        print("--------------- question_1 ---------------")
        print(q1_df.head().to_string())
    return q1_df

def question_2(print_val):
    
    q2_df = question_1(None)
    q2_df['Country'] = q2_df['Country'].apply(lambda x: x.lstrip().split('(')[0].strip(' '))
    q2_df = q2_df.set_index('Country')
    columns = ['summer_rubbish', 'summer_total' , 'winter_total']
    q2_df = q2_df.drop(columns, axis=1)
    #q2_df.to_csv('q2.csv')
    if print_val:
        print("--------------- question_2 ---------------")
        print(q2_df.head().to_string())

    return q2_df

def question_3(print_val):
    
    q3_df = question_2(None)
    q3_df = q3_df.dropna(axis=0, how='all')
    #q3_df.to_csv('q3.csv')
    if print_val:
        print("--------------- question_3 ---------------")
        print(q3_df.tail(10).to_string())

    return q3_df

def question_4():

    q4_df = question_3(None)
    #q4_df.to_csv('output.csv')
    q4_df = convert_to_numeric(q4_df)
    answer = q4_df.loc[(q4_df.summer_gold == q4_df['summer_gold'].max())]
    answer = answer.drop(answer.columns.difference(['summer_gold']),1)
    print("--------------- question_4 ---------------")
    print(answer['summer_gold'].to_string())

def question_5():

    q5_df = question_3(None)
    q5_df = convert_to_numeric(q5_df)
    q5_df['difference'] = abs(q5_df['summer_gold'] - q5_df['winter_gold'])
    answer = q5_df.loc[(q5_df.difference == q5_df['difference'].max())]
    answer = answer.drop(answer.columns.difference(['difference']),1)
    print("--------------- question_5 ---------------")
    print(answer.to_string())

def question_6():

    q6_df = question_3(None)
    q6_df = convert_to_numeric(q6_df)
    columns = ['summer_gold', 'summer_silver', 'summer_bronze', 'winter_gold', 'winter_silver', 'winter_bronze']
    q6_df = make_total_medal_column(q6_df, 'total_medals', columns)
    reduced_df = q6_df.drop(q6_df.columns.difference(['total_medals']),1)
    top_5 = reduced_df.head(5)
    bottom_5 = reduced_df.tail(5)
    print("--------------- question_6 ---------------")
    print("The top 5 medal earners are:")
    print(top_5.to_string())
    print()
    print("The bottom 5 medal earners are:")
    print(bottom_5.to_string())

def question_7():

    q7_df = question_3(None)
    q7_df = convert_to_numeric(q7_df)
    summer_totals = ['summer_gold', 'summer_silver', 'summer_bronze']
    winter_totals = ['winter_gold', 'winter_silver', 'winter_bronze']
    q7_df = make_total_medal_column(q7_df, 'summer_totals', summer_totals)
    q7_df = make_total_medal_column(q7_df, 'winter_totals', winter_totals)
    reduced_df = q7_df.drop(q7_df.columns.difference(['summer_totals','winter_totals']),1)
    reduced_df = reduced_df.head(10)
    reduced_df = make_total_medal_column(reduced_df, 'total_medals', ['summer_totals','winter_totals'])
    # print(reduced_df)
    reduced_df.drop(['total_medals'], axis=1, inplace=True)

    df2 = reduced_df.groupby(['summer_totals', 'winter_totals'], level=[0]).sum()
    #df2.plot(kind='barh', stacked=True)

    print("--------------- question_7 ---------------")
    plt.title('Medals for Winter and Summer Games')
    #plt.show()

def question_8():

    q8_df = question_3(None)
    q8_df = convert_to_numeric(q8_df)
    countries = ['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand']
    q8_df = q8_df[q8_df.index.isin(countries)]
    q8_df = q8_df.drop(q8_df.columns.difference(['winter_gold','winter_silver', 'winter_bronze']),1)
    #print(q8_df)
    
    print("--------------- question_8 ---------------")
    #q8_df.plot.bar()
    #plt.show()

def question_9(print_val):

    q9_df = question_3(None)
    q9_df = convert_to_numeric(q9_df)
    q9_df['summer_rank'] = 0
    q9_df['winter_rank'] = 0
    q9_df['summer_rank'] = q9_df.apply(lambda x: 0 if q9_df['summer_participation'].any() == 0 else \
                        (5*q9_df['summer_gold'] + 3*q9_df['summer_silver'] + q9_df['summer_bronze'])/q9_df['summer_participation'])
    q9_df['winter_rank'] = q9_df.apply(lambda x: 0 if q9_df['winter_participation'].any() == 0 else \
                        (5*q9_df['winter_gold'] + 3*q9_df['winter_silver'] + q9_df['winter_bronze'])/q9_df['winter_participation'])
    q9_df.fillna(value=0,inplace=True)
    q9_df.sort_values(by=['summer_rank'], ascending=False, inplace=True)
    result = q9_df.drop(q9_df.columns.difference(['summer_rank']),1).head(5)
    if print_val:
        print("--------------- question_9 ---------------")
        print(result.to_string())
    return q9_df

def question_10():
    
    q10_df = question_9(None)
    continents = pd.read_csv('Countries-Continents.csv')
    q10_df.sort_values(by=['winter_rank'], ascending=False, inplace=True)

    result = pd.merge(q10_df,continents, how='left', on='Country')
    result.fillna(value='Unsorted', inplace=True)
    result.set_index('Country', inplace=True)
    result = result.drop(result.columns.difference(['summer_rank', 'winter_rank', 'Continent']),1)

    #result.to_csv('result.csv')
    colours = {'Oceania' : 'blue', 'North America' : 'red', 'Europe' : 'green', 'Africa' : 'black', 'South America' : 'pink', 'Asia' : 'yellow', 'Unsorted' : 'gray'}
    plt.scatter(result['summer_rank'], result['winter_rank'], c=result['Continent'].apply(lambda x: colours[x]), s=10, alpha=0.85)

    c_legend = [mpatches.Patch(facecolor = value, label = key, alpha = 0.7) for key, value in colours.items()]
    plt.legend(handles = c_legend, loc='best')

    for i,lbl in enumerate(result.index):
        plt.annotate(lbl, (result['summer_rank'][i], result['winter_rank'][i]),fontsize = 8)

    plt.grid(True)
    plt.xlabel('Summer Rate')
    plt.ylabel('Winter Rate')

    plt.show()
    print("--------------- question_10 ---------------")
    

if __name__ == "__main__":
    q1_df = question_1(1)
    q2_df = question_2(1)
    q3_df = question_3(1)
    question_4()
    question_5()
    question_6()
    question_7()
    question_8()
    q9_df = question_9(1)
    question_10()