import pandas as pd
import re
from file_manager import merge_csv_files_in_directory
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

"""
언급량 데이터 시각화

- 

"""


data_year = '2020'

#2020년도별 파일 merge
directory = './trendAnalysis/buzz_data/'
#merge_csv_files_in_directory(directory, data_year)

#merge한 파일 들고 오기 
all_buzz_df = pd.read_csv("./trendAnalysis/buzz_data/buzz_data_merged_2020.csv")
print(all_buzz_df.head())
print(all_buzz_df.info())

all_buzz_df['date'] = pd.to_datetime(all_buzz_df['date'])
print(all_buzz_df.info())
print(all_buzz_df[:10])

#그래프 그리기
plt.figure(figsize=(10,5))
sns.lineplot(data=all_buzz_df, x=all_buzz_df['date'], y=all_buzz_df['buzz'], hue="day")