import pandas as pd
from konlpy.tag import Mecab
from collections import Counter
from ast import literal_eval
from datetime import datetime

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
stop_words = ['지난해','지난','대통령','정치','장관','정책','한국','사업','정부','지원','종합','경제','코로나','올해',
              '기업','지역','사업','시장','산업','한국','추진','관련','사회','국민','상황','가능','서울','필요','이번',
              '경우','대상','우리','총선','후보','실장','국회','공천','공약','국회의원','지역구','이번','여당','기업',
              '회의','선거','출마','보수','위원장','국내','행위','출시','이후','바이러스','기사','청와대','전년','우한',
              '중국','지금','도시','기술','제품','시민','부패','검찰','인사','폐렴','대표','수사','민주당','그룹','이날',
              '분류','의원','설명','기준','운영','공급','위원회','이후','경기','사람','방안','활용','금융','기업','계획',
              '경우','문제','기관','규모','국가','이상','미국','때문','평가','이상','관리','대책','강화','확대','조사',
              '발표','연구','예정','개발','대응','분야','개선','의료','혁신','제도','대비','협력','성장','센터','진행',
              '투자','마련','전망','미래','확산','강조','위기','추가','적극','시간','가격','교수','발생','관계자',
              '최근','서비스','현재','정보','전망','규제','증가','결과','세계','문화','시설','활동','시작','생각','주요',
              '효과','전국','영향','업무','우려','구축','기간','사태','지방','지급','수출','과정','행정','시행','수준','제공',
              '위원','은행','상승','피해','감소','지속','조치','문재인','생산','결정','주장','사건','과장','확진','환자',
              '분기','단지','사업자','선정','서울시','서울','최대','경기도','저희','사실','부분','나라','중요','이유','무엇',
              '당시','다음','오전']

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

#파일명
data_year = '2020_'
timestamp = data_year + datetime.now().strftime("%m%d")

#2020년도 : 309300건
news_df = pd.read_csv("./trendAnalysis/news_data/processed_data_2020_0510.csv")
print("news_df :", news_df.shape)
print(news_df.head())

# #공백기준으로 본문 내용 split
news_df['split_content'] = news_df['content'].str.split()
print("\n 공백기준으로 본문 split :", news_df[:5])

print("---------------------품사부착 및 파일 저장 (PoS Tagging)------------------------")

# #명사 추출
# news_df['noun_tokens'] = noun_tagging(news_df['split_content'])
# print("\n 본문 명사만 추출 : ", news_df['noun_tokens'][:5])
# print(news_df.shape)
# print(news_df.head())

# # split 데이터를 각 하나의 리스트로 만들기 # split 데이터를 각 하나의 리스트로 만들기 
# news_df['flatted_noun_tokens'] = news_df['noun_tokens'].apply(flatten_nested_list)
# print('flatted_noun_tokens', news_df['flatted_noun_tokens'].head())

# #mecab 실행시 메모리 부족 에러로 mecab 결과 파일로 저장
# mecab_filename = f'./trendAnalysis/news_data/news_mecab_{timestamp}.csv'
# news_df[['flatted_noun_tokens','date']].to_csv(mecab_filename, index=False, encoding='utf-8-sig')

print("--------------------- 불용어 처리 및 최빈값 조회 ------------------------")

#파일 데이터 프레임 형태로 불려오기 
news_df = pd.read_csv("./trendAnalysis/news_data/news_mecab_2020_0510.csv")
print(news_df.shape)
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
print(news_df.shape)

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in news_df['content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(40)
print(" ****불용어 처리 후 최빈어 조회**** : ", most_common_words) 

#총 데이터 개수 : 309300
# news_df[['content','inp_date']].to_csv('./trendAnalysis/news_data/news_data_tokenized_2020.csv' , index=False, encoding='utf-8-sig')
filename = f'./trendAnalysis/news_data/news_tokenized_{timestamp}.csv'
news_df.to_csv(filename, index=False, encoding='utf-8-sig')
