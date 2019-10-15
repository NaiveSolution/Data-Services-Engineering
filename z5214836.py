import pandas as pd

#pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.option_context('display.max_columns', None, 'display.max_rows', None)

def read_csv_files(file1, file2):

    summer_df = pd.read_csv('Olympics_dataset1.csv')
    winter_df = pd.read_csv('Olympics_dataset2.csv')
    
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
    if print_val:
        print("--------------- question_2 ---------------")
        print(q2_df.head().to_string())

    return q2_df

def question_3(print_val):
    
    q3_df = question_2(None)
    q3_df = q3_df.dropna(axis=0, how='all')
    if print_val:
        print("--------------- question_3 ---------------")
        print(q3_df.tail(10).to_string())

    return q3_df

def question_4():
    print("--------------- question_4 ---------------")
    pass

def question_5():
    print("--------------- question_5 ---------------")
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