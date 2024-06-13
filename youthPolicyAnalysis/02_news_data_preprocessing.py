import pandas as pd
from ast import literal_eval
from collections import Counter
from preprocessor.cleanser import keyword_cleanser
from preprocessor.tokenizer import extract_pos_tag
from utils import merge_yearly_csv

"""
뉴스 데이터 전처리 

- 정규표헌식을 통한 특수 문자 제외
- 여러개의 공백 제거 
- 결측치 제외 
- 뉴스 본문과 날짜 컬럼만 추출
- 140자 이하 뉴스 제외(광고나 짧은 뉴스는 본문 내용이 의미가 없다고 봄)
- 날짜포맷 변환 ("YYYY-mm-dd" 형태로 사용)

"""
#병합할 데이터 년도 및 키워드
year = "2023"
keyword = "정책"

#저장 및 읽을 파일의 위치
directory = './youthPolicyAnalysis/data/news/'
#수집한 csv파일 데이터 합치기 
#merged_file = merge_yearly_csv(directory, year, keyword)

merged_file = "./youthPolicyAnalysis/data/news/news_merged_정책_2324.csv"
#merge한 파일 들고 오기 
all_news_df = pd.read_csv(merged_file)

#결측지 제거 전
print("결측지 제거 전 :" , all_news_df.shape)

#결측지 제거 후
all_news_df = all_news_df.dropna(axis=0)[:10]
print("결측지 제거 후 : ", all_news_df.shape)

#뉴스 본문과 날짜 컬럼만 추출
news_content_df = all_news_df[['inp_date',"content","origin_url"]]
print(news_content_df[:10])

# 복사본의 열 수정
news_content_df.loc[:, 'content'] = news_content_df['content'].apply(keyword_cleanser.reduce_multiple_spaces)
#print(content_df_copy.head())

# NaN 값을 빈 문자열로 대체
news_content_df['content'] = news_content_df['content'].fillna('').astype(str)

#데이터 전처리 
news_content_df['content'] = news_content_df['content'].map(keyword_cleanser.remove_special)
print("특수 문제 제거 후 : ", news_content_df['content'].head())

#날짜 변환
news_content_df['date'] = pd.to_datetime(news_content_df['inp_date'])
news_content_df['date'] = news_content_df['date'].dt.strftime("%Y-%m-%d")
print(news_content_df['date'][:10])

#content 기사 길이가 140자 이하인 경우 제외
news_content = news_content_df.loc[news_content_df['content'].str.len() > 140]
print(news_content.info())
print("140자 이하인 경우 제외한 후: ", news_content.head())

# 전처리한 데이터 파일로 저장
filename = f'{directory}processed_data_{keyword}_{year}.csv'
news_content[['date','content','origin_url']].to_csv(filename, index=False, encoding='utf-8-sig')

"""
뉴스 데이터 토큰화 

- 단어 공백으로 split
- mecab을 이용한 명사 추출
- NaN값 제외
- 한글자 제외 (추출된 한글자는 대부분 조사에 해당하여 제외 시킴)
- 최빈어 조회
- 불용어 제거 

"""

news_df = pd.read_csv(f"{directory}processed_data_{keyword}_{year}.csv")
print("news_df :", news_df.shape)
print(news_df.head())

#공백기준으로 본문 내용 split
news_df['split_content'] = news_df['content'].str.split() 
print("\n 공백기준으로 본문 split :", news_df[:5])

print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

#명사 추출
news_df['noun_tokens'] = extract_pos_tag.noun_tagging(news_df['split_content'])
print("\n 본문 명사만 추출 : ", news_df['noun_tokens'][:5])
print(news_df.shape)
print(news_df.head())

# split 데이터를 각 하나의 리스트로 만들기 
news_df['flatted_nouns'] = news_df['noun_tokens'].apply(keyword_cleanser.flatten_list)
print('flatted_nouns', news_df['flatted_nouns'].head())

# 대용량 뉴스 데이터로 인하여 mecab의 결과를 파일로 저장
mecab_file_name = f'{directory}news_mecab_{keyword}_{year}.csv'

news_df[['date','flatted_nouns','origin_url']].to_csv(mecab_file_name, index=False, encoding='utf-8-sig')
print(news_df.head())
print(news_df.shape)

print("--------------------- 불용어 처리 및 최빈값 조회 ------------------------")

#파일 데이터 프레임 형태로 불려오기
news_df = pd.read_csv(mecab_file_name)
print(news_df.shape)
print(news_df.head())

# 리스트 형태로 복원 (문자열을 실제 리스트로 변환)
# literal_eval : 자료형(딕션너리, 리스트) 객체로 변환
news_df['flatted_nouns'] = news_df['flatted_nouns'].apply(literal_eval)
print(news_df['flatted_nouns'].head())

# NaN값 제외
news_df = news_df.dropna()
print("NaN값 제외 : ", news_df.info())

#불용어 처리
stopwords_file = "./youthPolicyAnalysis/preprocessor/cleanser/policy.txt"
news_df['content'] = news_df['flatted_nouns'].apply(lambda x: keyword_cleanser.process_text_with_stop_words(stopwords_file, x))

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in news_df['content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(40)
print("불용어 처리 후 최빈어 조회 : ", most_common_words) 

#전처리 된 데이터 저장
filename = f'{directory}news_tokenized_{keyword}_{year}.csv'
news_df[['date','content','origin_url']].to_csv(filename, index=False, encoding='utf-8-sig')