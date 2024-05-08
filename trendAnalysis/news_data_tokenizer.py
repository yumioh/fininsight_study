import pandas as pd
from konlpy.tag import Mecab
from collections import Counter
from ast import literal_eval

"""
뉴스 데이터 토큰화 

- 단어 공백으로 split
- mecab을 이용한 명사 추출
- NaN값 제외
- 한글자 제외 (추출된 한글자는 대부분 조사에 해당하여 제외 시킴)
- 최빈어 조회
- 불용어 제거 

"""

#불용어
stop_words = ['지난해','지난','대통령','정치','장관','정책','한국','사업','정부','지원','종합','경제','코로나','올해'
              '기업','지역','사업','시장','산업','한국','추진','관련','사회','국민','상황','가능','서울','필요','이번'
              '경우','대상','우리','총선','후보','실장','국회','공천','공약','국회의원','지역구','이번','여당',
              '회의','선거','출마','보수','위원장','국내','행위','출시','이후','바이러스','기사','청와대','전년']

#불용어 처리 함수
def remove_stopwords(tokens):
    return [token for token in tokens if token not in stop_words and len(token) > 1]

#한글자씩 제외 함수
def remove_single_char_tokens(tokens):
    return [token for token in tokens if isinstance(token, str) and len(token) > 1]

#중첩된 리스트를 하나의 리스트로 만드는 함수
def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

#mecab을 이용하여 명사만 추출 함수
def noun_tagging(df) :
  mecab = Mecab('C:\mecab\share\mecab-ko-dic')
  return df.apply(lambda x: [mecab.nouns(word) for word in x]) 

#2020년도 : 325805건
# news_df = pd.read_csv("./trendAnalysis/news_data/processed_data_2020.csv")
# print(news_df.head())

# #공백기준으로 본문 내용 split
# news_df['split_content'] = news_df['content'].str.split()
# print("\n 공백기준으로 본문 split :", news_df[:5])

print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

#명사 추출
# news_df['noun_tokens'] = noun_tagging(news_df['split_content'])
# print("\n 본문 명사만 추출 : ", news_df['noun_tokens'][:5])
# print(news_df.shape)
# print(news_df.head())

# # split 데이터를 각 하나의 리스트로 만들기 # split 데이터를 각 하나의 리스트로 만들기 
# news_df['flatted_noun_tokens'] = news_df['noun_tokens'].apply(flatten_nested_list)
# print(news_df['flatted_noun_tokens'][:10])

# #mecab 실행시 메모리 부족 에러로 mecab 결과 파일로 저장
# news_df[['flatted_noun_tokens','inp_date']].to_csv('./trendAnalysis/news_data/news_mecab_2020.csv', index=False, encoding='utf-8-sig')

print("--------------------- 불용어 처리 및 최빈값 조회 ------------------------")

#파일 데이터 프레임 형태로 불려오기 
news_df = pd.read_csv("./trendAnalysis/news_data/news_mecab_2020.csv")
print(news_df.head())

# 리스트 형태로 복원 (문자열을 실제 리스트로 변환)
# literal_eval : 자료형(딕션너리, 리스트) 객체로 변환
news_df['flatted_noun_tokens'] = news_df['flatted_noun_tokens'].apply(literal_eval)

# NaN값 제외
news_df = news_df.dropna()
print("nan값 제외 : ", news_df.info())

#한글자는 제외
news_df['flatted_noun_tokens'] = news_df['flatted_noun_tokens'].apply(remove_single_char_tokens)
print("한글자 제외 : ", news_df['flatted_noun_tokens'].head()) 

# 최빈어를 조회하여 불용어 제거 대상 선정
# most_common_tag = [word for tokens in news_df['flatted_noun_tokens'] for word_list in tokens for word in str(word_list).split()]
# most_common_words = Counter(most_common_tag).most_common(30)
# print("****불용어 처리 전 최빈어 조회**** : ", most_common_words) 

#불용어처리 
news_df['content'] = news_df['flatted_noun_tokens'].apply(remove_stopwords) 
print("\n 불용어 처리 : ", news_df['content'].head())
print(news_df.info())

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in news_df['content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(30)
print(" ****불용어 처리 후 최빈어 조회**** : ", most_common_words) 

#총 데이터 개수 : 309300
# news_df[['content','inp_date']].to_csv('./trendAnalysis/news_data/news_data_tokenized_2020.csv' , index=False, encoding='utf-8-sig')
news_df['content'].to_csv('./trendAnalysis/news_data/news_data_tokenized_2020.csv' , index=False, encoding='utf-8-sig')

# 불용어 처리 및 최빈값 조회 확인
# 버즈량과 감정분석 데이터 2020년도 수집 
# LDA 모델링 및 워드 클라우드 시각화 