import pandas as pd
from konlpy.tag import Mecab
import re
from ast import literal_eval
from collections import Counter

"""
댓글 데이터 전처리

- 여러 공백, 특수 문자 제거, 날짜변환

"""

#불용어
stop_words = ['지난해','지난','대통령','정치','장관','한국','사업','정부','지원','종합','경제','코로나','올해',
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
              '당시','다음','오전','내년','개월','가구','부산','노력','기반','모두','등의','내용','단체','포함','사용','본부',
              '지적','조성','예상','조정','논의','의견','예산','윤석열','입장','달러','가운데','회장','정원','준비','전문',
              '인하','중심','신청','공공의','발전','의대','의사','병원','대학','참여','증원','기대','체계','전공의','도입',
              '국제','확보','등이','정도','섹션','추천','현장','관계','개최','행상','연구원','성과','방향','하락','역할','최고',
              '전문가','유지','학생','기록','핵심','전략','공개','목표','건설','참석','반영','만큼','행사','경영','요구','적용','검토',
              '격월','구간','고려','모집','무작위','등록','광주','시대','오후','이하','얘기','전남','대한','민국','대한민국','프로그램',
              '통합','특별','하나','기획','조억','재정','방역','업체','신종','자의','생활','주민','학교','기존','재난','단계','일부',
              '확인','세대','우수','공사','정부','민주','이재명','개딸','인간','정권','좌파','북한','박근혜','자기','어디','죄명','누가',
              '이게','공산당']


# 여러 개의 공백을 한 개의 공백으로 줄이는 함수
def reduce_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)

def remove_special(text):
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", ' ', text) # 특수 문자 제거
    text = re.sub(r'[^a-zA-Z0-9\sㄱ-ㅎ가-힣]', '', text)   
    text = pattern_onlyKorean.sub('',text)
    return text

#mecab을 이용하여 명사만 추출 함수
def noun_tagging(df) :
  mecab = Mecab('C:\mecab\share\mecab-ko-dic')
  return df.apply(lambda x: [mecab.nouns(word) for word in x]) 

#중첩된 리스트를 하나의 리스트로 만드는 함수
def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

#불용어 처리 함수
def remove_stop_words(tokens):
   return [token for token in tokens if token not in stop_words and len(token) > 1]

subject = "정책"
year = "2023"
mon = "09"

comments_df = pd.read_csv("./youthPolicyAnalysis/data/news/comments_정책_2023-09.csv")

#결측치 확인
comments_df = comments_df.dropna(axis=0)

# NaN 값을 빈 문자열로 대체
comments_df['contents'] = comments_df['contents'].fillna('').astype(str)
print(comments_df.head())

#데이터 전처리 
comments_df['contents'] = comments_df['contents'].map(remove_special)
print("######## 전처리된 데이터 #######")
print(comments_df['contents'].head())

# 여러공백 제거
comments_df['contents'] = comments_df['contents'].apply(reduce_multiple_spaces)
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
# comments_df['noun_tokens'] = noun_tagging(comments_df['split_content'])
# print("\n 본문 명사만 추출 : ", comments_df['noun_tokens'][:5])
# print(comments_df.shape)
# print(comments_df.head())

# #split 데이터를 각 하나의 리스트로 만들기 
# comments_df['flatted_nouns'] = comments_df['noun_tokens'].apply(flatten_list)
# print('flatted_nouns', comments_df.head())

# comments_data = comments_df[['date','flatted_nouns']]

# # #mecab 실행시 메모리 부족 에러로 mecab 결과 파일로 저장
# mecab_filename = f'./youthPolicyAnalysis/data/news/comments_mecab_{subject}_{year}_{mon}.csv'

# comments_data.to_csv(mecab_filename, index=False, encoding='utf-8-sig')
# print(comments_data.head())
# print(comments_data.shape)

print("--------------------- 불용어 처리 및 최빈값 조회 ------------------------")

#파일 데이터 프레임 형태로 불려오기
comments_data = pd.read_csv("./youthPolicyAnalysis/data/news/comments_mecab_정책_2023_09.csv")
# 리스트 형태로 복원 (문자열을 실제 리스트로 변환)
# literal_eval : 자료형(딕션너리, 리스트) 객체로 변환
comments_data['flatted_nouns'] = comments_data['flatted_nouns'].apply(literal_eval)
print(comments_data.head())

comments_data = comments_data.dropna()
print("nan값 제외 : ", comments_data.info())

#불용어처리 
comments_data['content'] = comments_data['flatted_nouns'].apply(remove_stop_words) 
print("\n 불용어 처리 : ", comments_data['content'].head())
print(comments_data.shape)

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in comments_data['content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(30)
print("****불용어 처리 후 최빈어 조회**** : ", most_common_words) 