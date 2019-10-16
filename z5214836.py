import pandas as pd

#pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.option_context('display.max_columns', None, 'display.max_rows', None)

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
    answer.drop(answer.columns.difference(['summer_gold']),1, inplace=True)
    print("--------------- question_4 ---------------")
    print(answer.to_string())

def question_5():
    q5_df = question_3(None)
    q5_df = convert_to_numeric(q5_df)
    q5_df['difference'] = abs(q5_df['summer_gold'] - q5_df['winter_gold'])
    answer = q5_df.loc[(q5_df.difference == q5_df['difference'].max())]
    answer.drop(answer.columns.difference(['difference']),1, inplace=True)
    print("--------------- question_5 ---------------")
    print(answer.to_string())
    pass

def question_6():
    print("--------------- question_6 ---------------")
    pass

def question_7():
    print("--------------- question_7 ---------------")
    pass

def question_8():
    print("--------------- question_8 ---------------")
    pass

def question_9():
    print("--------------- question_8 ---------------")
    pass

def question_10():
    print("--------------- question_8 ---------------")
    pass

if __name__ == "__main__":
    q1_df = question_1(1)
    q2_df = question_2(1)
    q3_df = question_3(1)
    question_4()
    question_5()
    question_6()
    question_7()
    question_8()
    question_9()
    question_10()