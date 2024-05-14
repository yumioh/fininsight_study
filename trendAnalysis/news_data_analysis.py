import pandas as pd
import os
from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel
from ast import literal_eval
from dotenv import load_dotenv
from datetime import datetime
from data_analysis_manager import lda_modeling_and_visualization, create_wordcloud


#제외할 키워드
def remove_keywords(tokens, keywords):
    return [token for token in tokens if token not in keywords]

def main():
    """
    뉴스 데이터 분석

    - 날짜별 키워드별 데이터 추출
    - LDA 모델링 
    - 워드 클라우드 

    """
    #워드 클라우드 폰트 경로
    load_dotenv()
    path = os.getenv('font_path') 

    #전처리된 뉴스 파일 가져오기 
    #2020년도 : 309300건
    #news_df = pd.read_csv("./trendAnalysis/news_data/news_tokenized_2020_0510.csv")
    news_df = pd.read_csv("./trendAnalysis/news_data/news_tokenized_act_2020.csv")
    print(news_df.shape)
    print(news_df.head())

    #데이터 프레임의 각 행을 리스트 형태로 변환
    #문자열로 저장된 리스트를 실제 리스트로 변환
    news_df['tokens'] = news_df['content'].apply(literal_eval)

    # 날짜를 datetime 형식으로 변환
    news_df['date'] = pd.to_datetime(news_df['date'])

    #해당하는 키워드 행만 찾기
    
    
    start_date = '2020-01-01'
    end_date = '2020-08-02'

    data_year = '2020'
    subject = "act_bf"
    keywords = ['정책','청년']
     
    #이중에 하나라도 포함된 행 선택
    # news_df['tokens'].apply(lambda tokens: any(keyword in tokens for keyword in keywords))
    # 해당하는 모든 키워드 선택
    # news_df['tokens'].apply(lambda tokens: all(keyword in tokens for keyword in keywords))
    # 하나의 키워드
    #news_df['tokens'].apply(lambda tokens: '청년' in tokens)
   
    # 특정 기간과 해당하는 키워드 행만 추출
    filtered_df = news_df[
        (news_df['date'] >= start_date) & 
        (news_df['date'] <= end_date) & 
        (news_df['tokens'].apply(lambda tokens: all(keyword in tokens for keyword in keywords)))
    ]
    print("-----------------------------------------")   
    print(f"특정 기간 동안 {subject}가 포함된 뉴스행 추출 : ", filtered_df.shape)
    print("-----------------------------------------")
    print(filtered_df.head())

    #filtered_df.to_csv(f"./trendAnalysis/news_data/keyword_{subject}_{data_year}.csv", index=False, encoding="utf-8-sig")
    
    #시각화를 위해 청년 키워드만 삭제
    #filtered_df['tokens'] = filtered_df['tokens'].apply(lambda tokens: remove_keywords(tokens, ['교육']))
    filtered_df.loc[:, 'tokens'] = filtered_df['tokens'].apply(lambda tokens: remove_keywords(tokens, keywords))

    print("---------------------중복된 키워드 추출------------------------")
    #시행 기간 나누기 
    start_date_bf = '2020-01-01'
    end_date_bf = '2020-08-02'
    start_date_af = '2020-08-03'
    end_date_af = '2020-12-31'
    filtered_df_bf = filtered_df_bf[(filtered_df_bf['date'] >= start_date_bf) & (filtered_df_bf['date'] <= end_date_bf)]
    fileter_df_af = fileter_df_af[(fileter_df_af['date'] >= start_date_af) & (fileter_df_af['date'] <= end_date_af)]

    #두 공통 키워드 추출
    common_keywords = filtered_df_bf.intersection(fileter_df_af)
    print(common_keywords)

    
    # 공통 키워드 제거 함수
    def remove_common_keywords(keyword_list):
        return [keyword for keyword in keyword_list if keyword not in common_keywords]
    
    # 각 데이터 프레임의 키워드 열에서 공통 키워드 제거
    df1['keywords'] = df1['keywords'].apply(remove_common_keywords)
    df2['keywords'] = df2['keywords'].apply(remove_common_keywords)


    print("---------------------워드 클라우드------------------------")

    """"
    워드 클라우드 순서
    1. 단어 빈도 계산
    2. 워드 클라우드 생성
    """
    # 나눔고딕 폰트 경로 (예시: Windows의 경우) 
    font_path = path + "NanumBarunGothic.ttf"
    filename = f'./trendAnalysis/news_data/visualization/wordcloud_{subject}_{data_year}.png'

    # 워드 클라우드 생성 함수 호출
    create_wordcloud(filtered_df, font_path, filename)

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
    
    lda_modeling_and_visualization(corpus_TFIDF, dictionary, data_year, subject)

if __name__ == "__main__":
    main()

