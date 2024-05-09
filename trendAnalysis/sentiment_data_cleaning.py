import pandas as pd
import re
from file_manager import merge_csv_files_in_directory
from datetime import datetime

"""
감정분석 데이터 시각화

- 

"""

data_year = '2020'

#2020년도별 파일 merge
directory = './trendAnalysis/sentiment_data/'
#merge_csv_files_in_directory(directory, data_year)

#merge한 파일 들고 오기 
all_sentiment_df = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_data_all_merged_2020.csv")
print(all_sentiment_df.head())