import pandas as pd
import os
from ast import literal_eval
from dotenv import load_dotenv
from collections import Counter
from visualization.wordcloud import create_wordcloud, create_wordcloud2
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
"""
- 뉴스 데이터 워드클라우드
- 언급량 데이터 막대그래프
- 감정분석 원 그래프

"""

# 가장 빈도가 높은 키워드 추출
def get_top_keywords(df, num_keywords=25):
    all_tokens = sum(df['content'], [])
    keyword_counts = Counter(all_tokens)
    top_keywords = keyword_counts.most_common(num_keywords)
    print("빈도 수가 높은 키워드 : ", top_keywords)
    #_ 변수를 무시하고 싶을때 사용하는 표현
    return set([keyword for keyword, _ in top_keywords])

#두 데이터 프레임에서 각각의 상위 키워드 추출하고, 공통된 키워드 반환
def find_common_keywords(df_first, df_second, num_keywords=25):
    top_keywords_first = get_top_keywords(df_first, num_keywords)
    top_keywords_second = get_top_keywords(df_second, num_keywords)
    common_keywords = list(top_keywords_first & top_keywords_second)
    print("공통된 키워드 추출 : ", common_keywords)
    return common_keywords

#제외할 키워드
def remove_keywords(tokens, keywords):
    return [token for token in tokens if token not in keywords]

# 해당하는 기간만 뉴스 데이터 뽑기
def filter_news(df, start_date, end_date, keywords):
    """
    - start_date : 필터링 시작 날짜 (포맷: 'YYYY-MM-DD')
    - end_date : 필터링 종료 날짜 (포맷: 'YYYY-MM-DD')
    - keywords : 필터링할 키워드 리스트

    """
    # 날짜 형식 변환
    condition_date = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
    condition = df['content'].apply(lambda tokens: set(keywords).issubset(tokens))
 
    return df[condition_date & condition]

#워드 클라우드 폰트 경로
load_dotenv()
path = os.getenv('font_path') 

"""
    뉴스 데이터 분석

    - 날짜별 키워드별 데이터 추출
    - 워드 클라우드

"""

def main():

    #개정전 : 2020/08/03 ~ 2020/12/31 (150일)
    news_df_before = pd.read_csv(f'{read_directory}news_tokenized_{keyword}_{year}.csv', parse_dates=['date'])
    print("개정 전 : ", news_df_before.shape)
    print("개정 전 : ", news_df_before.head())
    
    #개정후 : 2023/09/22 ~ 2024/02/20 (150일)
    news_df_after = pd.read_csv(f'{read_directory}news_tokenized_{keyword}_{year}.csv', parse_dates=['date'])
    print("개정 후 : ",  news_df_after.shape)
    print("개정 후 : ", news_df_after.head())

    #데이터 프레임의 각 행을 리스트 형태로 변환
    #문자열로 저장된 리스트를 실제 리스트로 변환
    news_df_before['content'] = news_df_before['content'].apply(literal_eval)
    news_df_after['content'] = news_df_after['content'].apply(literal_eval)
    
    #옵션값 넣기
    subject = ['정책']
    #subject = ['청년','정책']
    data_year = '2023'
    subject_pre = "youth_pre"
    subject_post = "youth_post"

    #개정 날짜 기준으로 전후 150일 기준(약 5개월) 
    #개정 전 기간
    start_date_pre = '2023-08-01'
    end_date_pre = '2023-08-15'

    #개정 후 기간
    start_date_post = '2023-08-16'
    end_date_post = '2024-08-31'

    # 특정 기간 동안 지정된 키워드 행만 찾기
    filtered_pre = filter_news(news_df_before, start_date_pre, end_date_pre, subject)
    filtered_post = filter_news(news_df_after, start_date_post, end_date_post, subject)

    print("-----------------------------------------")   
    print(f"{start_date_pre} ~ {end_date_pre} 기간 동안 {subject}가 포함된 뉴스행 추출 : ", filtered_pre.shape)
    print("-----------------------------------------")
    print(filtered_pre.head())

    print("-----------------------------------------")   
    print(f"{start_date_post} ~ {end_date_post} 기간 동안 {subject}가 포함된 뉴스행 추출 : ", filtered_post.shape)
    print("-----------------------------------------")
    print(filtered_post.head())

    # 공통 키워드 추출
    common_keywords = find_common_keywords(filtered_pre, filtered_post)
    filtered_pre.loc[:, 'content'] = filtered_pre['content'].apply(remove_keywords, args=(common_keywords,))
    print("개정 전 : ", filtered_pre.shape)

    filtered_post.loc[:, 'content'] = filtered_post['content'].apply(remove_keywords, args=(common_keywords,))
    print("개정 후 : ", filtered_post.shape)

    print("---------------------워드 클라우드------------------------")

    """"
    워드 클라우드 순서
    1. 단어 빈도 계산
    2. 워드 클라우드 생성
    """
    # 나눔고딕 폰트 경로 (예시: Windows의 경우) 
    font_path = path + "NanumBarunGothic.ttf"
    save_directory = "./img/"

    # 개정 전 워드클라우드 생성
    filename_pre = f'{save_directory}wordcloud_{subject_pre}_{data_year}_test.png'
    create_wordcloud(filtered_pre, font_path, filename_pre)

    # 개정 후 워드 클라우드 생성
    filename_post = f'{save_directory}wordcloud_{subject_post}_{data_year}_test.png'
    create_wordcloud2(filtered_post, font_path, filename_post)

    
    print("---------------------시행 전 LDA 학습 시작------------------------")
    
    # lda_modeling.lda_modeling_and_visualization(corpus_TFIDF, dictionary, data_year, subject_pre)

    print("---------------------시행 후 사전 생성------------------------")

    # #딕셔너리 생성 
    # dictionary = Dictionary(filtered_post['content'])
    # print("idword : ", list(dictionary.items())[:10])
    # #LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
    # corpus = [dictionary.doc2bow(tokens) for tokens in filtered_post['content']]
    # #tfidf로 벡터화 적용
    # tfidf = TfidfModel(corpus)
    # corpus_TFIDF = tfidf[corpus]
    
    print("---------------------시행 후 LDA 학습 시작------------------------")
    
    # lda_modeling.lda_modeling_and_visualization(corpus_TFIDF, dictionary, data_year, subject_post)


read_directory = './youthPolicyAnalysis/data/news/'
year = "2023"
keyword = "정책"

if __name__ == "__main__":
    main()

#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

"""
    언급량 데이터 시각화 : 막대그래프

"""
buzz_keyword = '정책'
interval = "month"
from_date = "2023-01-01"
to_date = "2023-12-31"

buzz_directory = './youthPolicyAnalysis/data/buzz/'

buzz_df = pd.read_csv(f'{buzz_directory}buzzdata_{buzz_keyword}_{interval}_{from_date}_{to_date}.csv')
print(buzz_df.shape)

# 날짜를 pandas datetime 형식으로 변환 (선택적)
buzz_df['date'] = pd.to_datetime(buzz_df['date'])
print(buzz_df['date'])
    
 # 날짜를 x축으로 설정
plt.figure(figsize=(10, 5))  # 그래프 크기 설정
plt.bar(buzz_df['date'], buzz_df['buzz'], color='skyblue', width=10)
    
# 그래프 타이틀 및 라벨 설정
plt.title('Monthly Buzz Data')
plt.xlabel('Date')
plt.ylabel('Buzz Count')
plt.xticks(rotation=45)   # x축 라벨 회전
    
# x축 날짜 포맷 변경 (선택적)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 날짜 포맷을 '년-월'로 설정
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # x축 눈금을 월 단위로 설정

#파일 저장
save_file = f'./img/buzz_graph_{buzz_keyword}_test.png'

# 그래프 보여주기
plt.tight_layout()  # 레이아웃 자동 조정
plt.savefig(save_file, dpi=300) 
plt.show()


"""
    감정분석 데이터 시각화 : 원그래프

"""

senti_keyword = '정책'
interval = "month"
from_date = "2020-01-01"
to_date = "2023-12-31"

senti_directory = './youthPolicyAnalysis/data/sentiment/'
#감정분석 파일 읽기
senti_df = pd.read_csv(f'{senti_directory}sentidata_{senti_keyword}_{interval}_{from_date}_{to_date}.csv')
print(senti_df.shape)


positive = len(senti_df[senti_df['score'] > 0])
negative = len(senti_df[senti_df['score'] < 0])
#neutral = len(senti_df[senti_df['score'] == 0])

# 원형 그래프 그리기 : 'Neutral' 제외
labels = ['Positive', 'Negative']
sizes = [positive, negative]
colors = ['#0079FF', '#FF204E']
explode = (0.1, 0.1)  # 각 섹션의 분리 정도

#파일 읽기
save_path = f"./img/sentiment_pie_{senti_keyword}_test.png"

plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Sentiment Distribution 20' to 23'")
plt.axis('equal')  # 원형 그래프를 원 모양으로 유지
plt.savefig(save_path, dpi=300)
plt.show()
 