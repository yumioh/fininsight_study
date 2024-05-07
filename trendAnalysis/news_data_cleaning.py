import pandas as pd
import re
from file_manager import merge_csv_files

##뉴스 전처리 

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

#2020년도별 파일 merge
directory = './trendAnalysis/news_data/'
year = '2020'
#merge_csv_files(directory, year)

#merge한 파일 들고 오기 
all_news_df = pd.read_csv("./trendAnalysis/news_data/merged_news_data_2020.csv")
# 결측지 제거 전 : 325870
print("raw data :" , all_news_df.shape)
#print(all_news_df.head())

#결측 여부 확인 : 325805
all_news_df = all_news_df.dropna(axis=0)
print("결측지 여부 확인 : ", all_news_df.shape)

#키워드 추출을 위해 내용만 컬럼만 추출
news_content_df = all_news_df[["content"]]
#print(selected_content_df)

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

# 전처리한 데이터 파일로 저장
#content_df_copy.to_csv('./trendAnalysis/news_data/processed_data_2020.csv' , index=False, encoding='utf-8-sig')


