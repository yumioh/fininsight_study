import pandas as pd
import glob
import os

"""
파일 관련 

- 수집한 데이터 CSV 파일 합치기

"""

def merge_csv_files(directory, year):
    # 지정된 연도의 파일 패턴 만들기
    file_pattern = os.path.join(directory, f'news_data_{year}*.csv')
    # 패턴에 맞는 파일 리스트 가져오기
    csv_files = glob.glob(file_pattern)
    
    # 데이터프레임 리스트 초기화
    dataframes = []
    
    # 각 파일을 읽고 데이터프레임 리스트에 추가
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # 데이터프레임 병합
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # 병합된 데이터를 새로운 파일로 저장
    combined_df.to_csv(os.path.join(directory, f'merged_news_data_{year}.csv'), index=False)
    print(f'Merged file saved: {directory}/merged_news_data_{year}.csv')

#사용 예
# directory = './trendPolicy/news_data/'
# year = '2020'
# merge_csv_files(directory, year)


