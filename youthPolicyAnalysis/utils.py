import pandas as pd
import os
import glob

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


#같은 년도끼리 파일 병합
def merge_yearly_csv(directory, year, keyword):
    
    # 하위 폴더에서 키워드와 연도에 맞는 파일 패턴을 생성
    file_pattern = os.path.join(directory, f'newsdata_{keyword}_{year}-*.csv')
    
    # 패턴에 맞는 모든 CSV 파일 가져옴
    csv_files = glob.glob(file_pattern)
    
    if not csv_files:
        print(f"No files found in {directory} for the keyword '{keyword}' and year {year}.")
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
    merged_filename = f'news_merged_{keyword}_{year}.csv'
    merged_file= os.path.join(directory, merged_filename)
    
    # 병합된 데이터를 새로운 파일로 저장
    combined_df.to_csv(merged_file, index=False)
    
    print(f'Merged file saved: {merged_file}')

    return merged_file

"""
    주어진 CSV 파일에서 특정 날짜 범위에 해당하는 데이터를 필터링하는 함수

    file_path (str): CSV 파일 경로
    start_date (str): 시작 날짜 (예: '2020-08-03')
    end_date (str): 종료 날짜 (예: '2020-12-31')

"""

def filter_news_by_date(file_path, start_date, end_date):
    # CSV 파일 읽기
    news_df = pd.read_csv(file_path)
    
    # 날짜 형식 변환
    news_df['inp_date'] = pd.to_datetime(news_df['inp_date'])
    
    # 필터링할 날짜 범위 정의
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # 지정된 날짜 범위에 해당하는 데이터만 필터링
    filtered_df = news_df[(news_df['inp_date'] >= start_date) & (news_df['inp_date'] <= end_date)]
    
    return filtered_df

"""
    주어진 CSV 파일을 연도와 월별로 나누어 별도의 CSV 파일로 저장하는 함수

    file_path (str): 입력 CSV 파일 경로
    output_dir (str): 출력 파일을 저장할 디렉토리 경로
    subject (str): 주제 또는 파일명에 포함될 문자열
    year (str): 연도 (예: '2020')

"""

def save_monthly_data(file_path, output_dir, subject, year):
    # CSV 파일 읽기
    news_df = pd.read_csv(file_path)
    
    # inp_date 필드를 datetime 형식으로 변환
    news_df['inp_date'] = pd.to_datetime(news_df['inp_date'])
    
    # 연도와 월별로 그룹화
    news_df['year_month'] = news_df['inp_date'].dt.to_period('M')
    
    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 각 그룹을 별도의 CSV 파일로 저장
    for period, group in news_df.groupby('year_month'):
        group = group.drop(columns=['year_month'])
        # 디렉토리 내에 파일을 저장
        output_file = os.path.join(output_dir, f'merged_{subject}_{year}_{period}.csv')
        group.to_csv(output_file, index=False)
        print(f"Saved {output_file} with shape {group.shape}")
    
    print("All monthly data files have been saved.")

    """
    주어진 CSV 파일 리스트를 하나로 합쳐서 새로운 CSV 파일로 저장하는 함수

    Parameters:
    file_list (list): 합칠 CSV 파일들의 경로가 포함된 리스트
    output_file (str): 합쳐진 결과를 저장할 파일 경로
    """

def merge_csv_files(file_list, output_file):

    dataframes = []

    for file in file_list:
        df = pd.read_csv(file)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    # 결과를 새로운 CSV 파일로 저장
    combined_df.to_csv(output_file, index=False)
    print(f"Combined file saved as {output_file}")

# 특수문자 제거 : 문자 전처리
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

#특수문자 제거 : 키워드 전처리시 사용
def remove_special(text):
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", ' ', text) # 특수 문자 제거
    text = re.sub(r'[^a-zA-Z0-9\sㄱ-ㅎ가-힣]', '', text)   
    text = pattern_onlyKorean.sub('',text)
    return text

# 여러 개의 공백을 한 개의 공백으로 줄이는 함수
def reduce_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)


#중첩된 리스트를 하나의 리스트로 만드는 함수
def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

# # 가장 빈도가 높은 키워드 추출
# def get_top_keywords(df, column_name, num_keywords=25):
#     all_tokens = sum(df[column_name], [])
#     keyword_counts = Counter(all_tokens)
#     top_keywords = keyword_counts.most_common(num_keywords)
#     print("빈도 수가 높은 키워드 : ", top_keywords)
#     #_ 변수를 무시하고 싶을때 사용하는 표현
#     return set([keyword for keyword, _ in top_keywords])

# def find_common_keywords(df_first, df_second, num_keywords=25):
#     top_keywords_first = get_top_keywords(df_first, num_keywords)
#     top_keywords_second = get_top_keywords(df_second, num_keywords)
#     common_keywords = list(top_keywords_first & top_keywords_second)
#     print("공통된 키워드 추출 : ", common_keywords)
#     return common_keywords

# 가장 빈도가 높은 키워드 추출
def get_top_keywords(df, column_name, num_keywords=25):
    all_tokens = sum(df[column_name].dropna().tolist(), [])
    keyword_counts = Counter(all_tokens)
    top_keywords = keyword_counts.most_common(num_keywords)
    print("빈도 수가 높은 키워드 : ", top_keywords)
    #_ 변수를 무시하고 싶을때 사용하는 표현
    return set([keyword for keyword, _ in top_keywords])

def find_common_keywords(df_first, df_second, column_name, num_keywords=25):
    top_keywords_first = get_top_keywords(df_first, column_name, num_keywords)
    top_keywords_second = get_top_keywords(df_second, column_name, num_keywords)
    common_keywords = list(top_keywords_first & top_keywords_second)
    print("공통된 키워드 추출 : ", common_keywords)
    return common_keywords

#제외할 키워드
def remove_keywords(tokens, keywords):
    return [token for token in tokens if token not in keywords]

def filter_long_words(word_list):
    return [word for word in word_list if len(word) > 1]