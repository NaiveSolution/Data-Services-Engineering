import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None, 'display.max_rows', None)

def main():
    summer_df = pd.read_csv('Olympics_dataset1.csv')
    winter_df = pd.read_csv('Olympics_dataset2.csv')
    print(summer_df)


if __name__ == "__main__":
    main()