import pandas as pd
import re
from file_manager import merge_csv_in_dir
from datetime import datetime

"""
뉴스 데이터 전처리 

- 정규표헌식을 통한 특수 문자 제외
- 여러개의 공백 제거 
- 결측치 제외 
- 뉴스 본문과 날짜 컬럼만 추출
- 140자 이하 뉴스 제외(광고나 짧은 뉴스는 본문 내용이 큰 의미가 없다고 봄)
- 날짜포맷 변환 (다른 데이터에서 날짜 포맷을 "YYYY-mm-dd" 형태로 사용)

"""

# 여러 개의 공백을 한 개의 공백으로 줄이는 함수
def reduce_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)

#특수문자 제거 
def remove_special(text):
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", text) # 특수 문자 제거
    text = re.sub(r'[^a-zA-Z0-9\sㄱ-ㅎ가-힣]', '', text)   
    text = pattern_onlyKorean.sub('',text)
    return text


#파일명 중복을 피하기 위함
data_year = '2024'
timestamp = data_year + datetime.now().strftime("%m%d")
subject = "정책"

#년도/ 키워드별 파일 merge
directory = './trendAnalysis/news_data/'
merged_file_path = merge_csv_in_dir(directory, data_year, subject)

#merge한 파일 들고 오기 
all_news_df = pd.read_csv(merged_file_path)
# 결측지 제거 전 : 325870
print("raw data :" , all_news_df.shape)
#print(all_news_df.head())

#결측 여부 확인 : 325805
all_news_df = all_news_df.dropna(axis=0)
print("결측지 여부 확인 : ", all_news_df.shape)

#키워드 추출을 위해 뉴스 본문과 날짜 컬럼만 추출
news_content_df = all_news_df[["content",'inp_date']]
print(news_content_df[:10])

# 데이터프레임 복사본 생성
content_df_copy = news_content_df.copy()

# 복사본의 열 수정
content_df_copy['content'] = content_df_copy['content'].apply(reduce_multiple_spaces)
#print(content_df_copy.head())

# NaN 값을 빈 문자열로 대체
content_df_copy['content'] = content_df_copy['content'].fillna('').astype(str)

#데이터 전처리 
content_df_copy['content'] = content_df_copy['content'].map(remove_special)
print("######## 전처리된 데이터 #######")
print(content_df_copy['content'].head())

#날짜 변환
content_df_copy['date'] = pd.to_datetime(content_df_copy['inp_date'])
content_df_copy['date'] = content_df_copy['date'].dt.strftime("%Y-%m-%d")
print(content_df_copy['date'][:10])

#content 기사 길이가 140자 이하인 경우 제외
content_df_copy = content_df_copy.loc[content_df_copy['content'].str.len() > 140]
print(content_df_copy.info())
print("content_df_copy : ", content_df_copy.head())

# 전처리한 데이터 파일로 저장
filename = f'./trendAnalysis/news_data/processed_data_{subject}_{data_year}.csv'
content_df_copy[['date','content']].to_csv(filename, index=False, encoding='utf-8-sig')


