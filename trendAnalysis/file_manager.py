import pandas as pd
import glob
import os

"""
파일 관련 

- 수집한 데이터 CSV 파일 합치기

"""
#뉴스데이터 한정
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


#해당하는 디렉토리에 년도가 동일한 파일만 병합
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
    
    return os.path.join(directory, merged_filename)

# 예시 사용법
#merge_csv_files_in_directory('./trendAnalysis/sentiment_data/', '2020')


#키워드와 년도가 동일한 경우 파일 병합
def merge_csv_in_dir(base_directory, year, keyword):
    # 병합할 파일이 있는 하위 폴더를 가리킵니다
    source_directory = os.path.join(base_directory, "data")
    
    # 하위 폴더에서 키워드와 연도에 맞는 파일 패턴을 생성합니다
    file_pattern = os.path.join(source_directory, f'*{keyword}*_{year}_*.csv')
    
    # 패턴에 맞는 모든 CSV 파일을 가져옵니다
    csv_files = glob.glob(file_pattern)
    
    if not csv_files:
        print(f"No files found in {source_directory} for the keyword '{keyword}' and year {year}.")
        return
    
    # 데이터프레임 리스트 초기화
    dataframes = []
    
    # 각 파일을 읽고 데이터프레임 리스트에 추가합니다
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # 데이터프레임 병합
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # 병합된 파일 이름 생성
    merged_filename = f'merged_{keyword}_{year}.csv'
    merged_file_path = os.path.join(base_directory, merged_filename)
    
    # 병합된 데이터를 새로운 파일로 저장
    combined_df.to_csv(merged_file_path, index=False)
    
    print(f'Merged file saved: {merged_file_path}')

    return merged_file_path

# 사용 예시
# 하나의 디렉토리를 입력받습니다
# base_directory = "./trendAnalysis/sentiment_data/"
# merge_csv_in_dir(base_directory, 2023, "정책")
