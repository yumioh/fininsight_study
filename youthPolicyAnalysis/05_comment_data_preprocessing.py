import pandas as pd
from konlpy.tag import Mecab
import re
from ast import literal_eval
from collections import Counter
from preprocessor.cleanser import keyword_cleanser
from preprocessor.tokenizer import extract_pos_tag

"""
댓글 데이터 전처리
- 여러 공백, 특수 문자 제거, 날짜변환

"""

subject = "policy"
year = "2324"

#댓글 데이터 불려오기
comments_df = pd.read_csv("./youthPolicyAnalysis/data/comment/comments_policy_2324.csv")
print("전처리 전 데이터 : ", comments_df.shape)

#결측치 확인
comments_df = comments_df.dropna(axis=0)

# NaN 값을 빈 문자열로 대체
comments_df['contents'] = comments_df['contents'].fillna('').astype(str)
print(comments_df.head())

#데이터 전처리 
comments_df['contents'] = comments_df['contents'].map(keyword_cleanser.remove_special)
print("######## 전처리된 데이터 #######")
print(comments_df['contents'].head())

# 여러공백 제거
comments_df['contents'] = comments_df['contents'].apply(keyword_cleanser.reduce_multiple_spaces)
print(comments_df.head())

#날짜 변환
comments_df['date'] = pd.to_datetime(comments_df['date'])
comments_df['date'] = comments_df['date'].dt.strftime("%Y-%m-%d")
print(comments_df.head())

comments_df = comments_df[['date','contents']]

comments_df['split_content'] = comments_df['contents'].str.split()
print("###공백 기준으로 본문 split :", comments_df[:5])

print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

# #명사 추출
comments_df['noun_tokens'] = extract_pos_tag.noun_tagging(comments_df['split_content'])
print("\n 본문 명사만 추출 : ", comments_df['noun_tokens'][:5])
print(comments_df.shape)
print(comments_df.head())

#split 데이터를 각 하나의 리스트로 만들기 
comments_df['flatted_nouns'] = comments_df['noun_tokens'].apply(keyword_cleanser.flatten_list)
comments_data = comments_df[['date','flatted_nouns']]

# #mecab 실행시 메모리 부족 에러로 mecab 결과 파일로 저장
mecab_filename = f'./youthPolicyAnalysis/data/comment/comments_mecab_{subject}_{year}.csv'
comments_data.to_csv(mecab_filename, index=False, encoding='utf-8-sig')
print(comments_data.head())
print("품사태깅 후 : ", comments_data.shape)

print("--------------------- 불용어 처리 및 최빈값 조회 ------------------------")

#파일 데이터 프레임 형태로 불려오기
comments_data = pd.read_csv(f"./youthPolicyAnalysis/data/comment/comments_mecab_policy_{year}.csv")
# 리스트 형태로 복원 (문자열을 실제 리스트로 변환)
# literal_eval : 자료형(딕션너리, 리스트) 객체로 변환
comments_data['flatted_nouns'] = comments_data['flatted_nouns'].apply(literal_eval)
print(comments_data.head())

comments_data = comments_data.dropna()
print("nan값 제외 : ", comments_data.info())

#불용어 처리
stopwords_file = "./youthPolicyAnalysis/preprocessor/cleanser/comment.txt"
comments_data['flatted_nouns'] = comments_data['flatted_nouns'].apply(lambda x: keyword_cleanser.process_text_with_stop_words(stopwords_file, x))

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in comments_data['flatted_nouns'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(30)
print("###### 불용어 처리 후 최빈어 조회 ###### : ", most_common_words) 

# 빈 리스트나 빈 문자열을 포함하는 행 삭제
comments_data = comments_data[comments_data['flatted_nouns'].apply(lambda x: len(x) > 0)]

filename = f'./youthPolicyAnalysis/data/comment/comments_tokenized_{subject}_{year}.csv'
comments_data[["date","flatted_nouns"]].to_csv(filename, index=False, encoding='utf-8-sig')