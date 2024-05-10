import pandas as pd
import os
from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel
from ast import literal_eval
from dotenv import load_dotenv
from datetime import datetime
from data_analysis_manager import lda_modeling_and_visualization, create_wordcloud


#청년 키워드 제외하고 모델링
def remove_keyword(tokens, keyword='청년'):
    return [token for token in tokens if token != keyword]

def main():
    """
    뉴스 데이터 분석

    - LDA 모델링 
    - 워드 클라우드 

    """
    #워드 클라우드 폰트 경로
    load_dotenv()
    path = os.getenv('font_path') 

    #파일명 중복을 피하기 위함
    data_year = '2020_'
    timestamp = data_year + datetime.now().strftime("%m%d_%H%M")

    #전처리된 뉴스 파일 가져오기 
    #2020년도 : 309300건
    news_df = pd.read_csv("./trendAnalysis/news_data/news_tokenized_2020_0510.csv")
    print(news_df.shape)
    print(news_df.head())

    # memory erorr로 인하여 30만개 중 5만 개만 샘플링데이터 랜덤으로 샘플림하여 모델링
    # news_df = news_df.sample(n=50000, random_state=42) 

    #데이터 프레임의 각 행을 리스트 형태로 변환
    #문자열로 저장된 리스트를 실제 리스트로 변환
    news_df['tokens'] = news_df['content'].apply(literal_eval)

    # 날짜를 datetime 형식으로 변환
    news_df['date'] = pd.to_datetime(news_df['date'])
    
    start_date = '2020-08-03'
    end_date = '2020-12-31'

     # '청년' 키워드를 포함한 뉴스만 추출 : 
    #youth_df = news_df[news_df['tokens'].apply(lambda tokens: '청년' in tokens)]
   
    keyword = "youth_act_after"

    # 특정 기간에 해당하는 데이터만 추출
    filtered_df = news_df[
        (news_df['date'] >= start_date) & 
        (news_df['date'] <= end_date) & 
        (news_df['tokens'].apply(lambda tokens: '청년' in tokens))
    ]
    print("특정 기간 동안 해당하는 키워드가 포함된 뉴스 추출 : ", filtered_df.shape)
    print(filtered_df.head())

    filtered_df.to_csv("./trendAnalysis/news_data/keyword.csv", index=False, encoding="utf-8-sig")

    #시각화를 위해 청년 키워드만 삭제
    filtered_df['tokens'] = filtered_df['tokens'].apply(lambda tokens: remove_keyword(tokens, '청년'))

    print("---------------------워드 클라우드------------------------")

    """"

    워드 클라우드 순서
    1. 단어 빈도 계산
    2. 워드 클라우드 생성

    """
    # 나눔고딕 폰트 경로 (예시: Windows의 경우) 
    font_path = path + "NanumBarunGothic.ttf"
    filename = f'./trendAnalysis/news_data/visualization/{keyword}_wordcloud_{timestamp}.png'

    # 워드 클라우드 생성 함수 호출
    create_wordcloud(filtered_df, font_path, filename)

    # # 모든 토큰을 하나의 리스트로 합치기
    # all_tokens = [token for tokens in news['tokens'] for token in tokens]

    # # 단어 빈도 계산
    # word_freq = Counter(all_tokens)

    # # 워드 클라우드 생성
    # wordcloud = WordCloud(
    #     font_path=font_path, 
    #     width=800, 
    #     height=400, 
    #     background_color='white', 
    #     max_words=100
    #     ).generate_from_frequencies(word_freq)

    # # 워드 클라우드 이미지를 파일로 저장
    # filename = f'./trendAnalysis/news_data/visualization/wordcloud_{timestamp}.png'
    # wordcloud.to_file(filename)

    """
    LDA 모델링 순서

    1. 각 문서에 대한 토큰화 적용
    2. 사전 생성
    3. 단어-문서 매트릭스 생성
    4. LDA 모델 구성 및 학습
    5. 중요단어 확인
    """

    print("---------------------사전 생성------------------------")

    #딕셔너리 생성 
    dictionary = Dictionary(filtered_df['tokens'])
    print("idword : ", list(dictionary.items())[:10])

    #LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
    corpus = [dictionary.doc2bow(tokens) for tokens in filtered_df['tokens']]

    #tfidf로 벡터화 적용
    tfidf = TfidfModel(corpus)
    corpus_TFIDF = tfidf[corpus]
    print("---------------------LDA 학습 시작------------------------")
    
    lda_modeling_and_visualization(corpus_TFIDF, dictionary, timestamp, keyword)

if __name__ == "__main__":
    main()

