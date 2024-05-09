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
# merge_csv_files('./trendPolicy/news_data/', '2020')


import os
import glob
import pandas as pd

def merge_csv_files_in_directory(directory, year):
    # 해당 디렉토리에서 주어진 연도에 맞는 파일 패턴 생성
    file_pattern = os.path.join(directory, f'*_{year}_*.csv')
    
    # 패턴에 맞는 모든 CSV 파일을 가져오기
    csv_files = glob.glob(file_pattern)
    
    if not csv_files:
        print(f"No files found in {directory} for the year {year}.")
        return
    
    # 데이터프레임 리스트 초기화
    dataframes = []
    
    # 각 파일을 읽고 데이터프레임 리스트에 추가
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # 데이터프레임 병합
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # 병합된 파일 이름 생성 (디렉토리의 이름 기반)
    base_name = os.path.basename(directory.rstrip('/\\'))
    merged_filename = f'{base_name}_merged_{year}.csv'
    
    # 병합된 데이터를 새로운 파일로 저장
    combined_df.to_csv(os.path.join(directory, merged_filename), index=False)
    
    print(f'Merged file saved: {os.path.join(directory, merged_filename)}')

# 예시 사용법
#merge_csv_files_in_directory('./trendAnalysis/sentiment_data/', '2020')



