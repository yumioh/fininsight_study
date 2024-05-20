import pandas as pd
import glob
import os


months = ['01','02','03','04','05','06']
monthss = ['07','08','09','10','11','12']

    
dataframe = []

for month in monthss:
    file_pattern = os.path.join("./trendAnalysis/news_data/data/", f'news_정책_2023_{month}.csv')

    csv_files = glob.glob(file_pattern)

    for file in csv_files:
        df = pd.read_csv(file)
        dataframe.append(df)
    

combinded_df = pd.concat(dataframe, ignore_index=True)
print(combinded_df.head())

combinded_df.to_csv("./trendAnalysis/news_data/merged_정책_2023_2ss.csv", index=False)
