import pandas as pd
import os
from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel
from ast import literal_eval
from dotenv import load_dotenv
from collections import Counter
from visualization.wordcloud import create_wordcloud
from visualization.lda_modeling import lda_modeling_and_visualization


#데이터 프레임에서 가장 빈도가 높은 키워드 추출
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

# 필터링된 뉴스 데이터를 반환하는 함수
def filter_news(df, start_date, end_date, keywords):
    """
    - start_date : 필터링 시작 날짜 (포맷: 'YYYY-MM-DD').
    - end_date : 필터링 종료 날짜 (포맷: 'YYYY-MM-DD').
    - keywords : 필터링할 키워드 리스트.
    - all_keywords : 모든 키워드가 포함되어야 하는지 여부 (기본값 True)
    """
    # 날짜 형식 변환
    condition_date = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
    
    # 키워드 필터링 조건 설정
    # if all_keywords:
    #     # 모든 키워드를 포함하는 행만 선택
    #     condition = df['content'].apply(lambda tokens: all(keyword in tokens for keyword in keywords))
    # else:
    #     # 주어진 키워드 중 하나라도 포함하는 행 선택
    #     condition = df['content'].apply(lambda tokens: any(keyword in tokens for keyword in keywords))

    condition = df['content'].apply(lambda tokens: set(keywords).issubset(tokens))
 
    return df[condition_date & condition]

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
    #2023.01 ~ 2024.05.14 : 675542건 : news_tokenized_정책_23_24_total.csv
    #2023.06.24 ~ 23.12.20 : 232169건 : news_tokenized_정책_23_24_filter_1.csv
    #개정전 : 2020/08/03 ~ 2020/12/31
    #개정후 : 2023/09/22 ~ 2023/12/20
    #news_df = pd.read_csv("./trendAnalysis/news_data/news_tokenized_act_2020.csv", parse_dates=['date'])
    news_df = pd.read_csv("./youthPolicyAnalysis/news_data/news_tokenized_정책_2020.csv", parse_dates=['date'])
    print(news_df.shape)
    print(news_df.head())

    #데이터 프레임의 각 행을 리스트 형태로 변환
    #문자열로 저장된 리스트를 실제 리스트로 변환
    news_df['content'] = news_df['content'].apply(literal_eval)
    
    #옵션값 넣기
    keywords = ['청년','정책']
    data_year = '2020'
    subject_pre = "comment_final"
    subject_post = "comment_final"

    #개정 날짜 기준으로 전후90일 기준(약 3개월) 
    #시행 전 기간
    start_date_pre = '2024-01-01'
    end_date_pre = '2024-08-02'
    #시행 후 기간
    start_date_post = '2020-08-03'
    end_date_post = '2020-12-31'
        
    #news_df['tokens'].apply(lambda tokens: '청년' in tokens)

    # 특정 기간 동안 지정된 키워드 행만 찾기
    filtered_df_first = filter_news(news_df, start_date_pre, end_date_pre, keywords)
    filtered_df_second = filter_news(news_df, start_date_post, end_date_post, keywords)

    print(filtered_df_first.shape) 
    print(filtered_df_first.head())

    filtered_df_first.to_csv("./youthPolicyAnalysis/data/news/news_정책_2024_filter.csv")
    print("완료")


    print("-----------------------------------------")   
    print(f"시행 전 기간 동안 {keywords}가 포함된 뉴스행 추출 : ", filtered_df_first.shape)
    print("-----------------------------------------")
    print(filtered_df_first.head())

    print("-----------------------------------------")   
    print(f"시행 후 기간 동안 {keywords}가 포함된 뉴스행 추출 : ", filtered_df_second.shape)
    print("-----------------------------------------")
    print(filtered_df_second.head())

    # 공통 키워드 추출
    common_keywords = find_common_keywords(filtered_df_first, filtered_df_second)
    filtered_df_first.loc[:, 'content'] = filtered_df_first['content'].apply(remove_keywords, args=(common_keywords,))
    print("시행전 : ", filtered_df_first.shape)

    filtered_df_second.loc[:, 'content'] = filtered_df_second['content'].apply(remove_keywords, args=(common_keywords,))
    print("시행후 : ", filtered_df_second.shape)

    print("---------------------워드 클라우드------------------------")

    """"
    워드 클라우드 순서
    1. 단어 빈도 계산
    2. 워드 클라우드 생성
    """
    # 나눔고딕 폰트 경로 (예시: Windows의 경우) 
    font_path = path + "NanumBarunGothic.ttf"
    
    # 시행 전 워드클라우드 생성
    filename_pre = f'./trendAnalysis/news_data/visualization/wordcloud_{subject_pre}_{data_year}.png'
    create_wordcloud(filtered_df_first, font_path, filename_pre)

    # 시행 후 워드 클라우드 생성
    filename_post = f'./trendAnalysis/news_data/visualization/wordcloud_{subject_post}_{data_year}.png'
    create_wordcloud(filtered_df_second, font_path, filename_post)

    """
    LDA 모델링 순서

    1. 각 문서에 대한 토큰화 적용
    2. 사전 생성
    3. 단어-문서 매트릭스 생성
    4. LDA 모델 구성 및 학습
    5. 중요단어 확인
    """

    print("---------------------시행 전 사전 생성------------------------")

    #딕셔너리 생성 
    dictionary = Dictionary(filtered_df_first['content'])
    print("idword : ", list(dictionary.items())[:10])
    #LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
    corpus = [dictionary.doc2bow(tokens) for tokens in filtered_df_first['content']]
    #tfidf로 벡터화 적용
    tfidf = TfidfModel(corpus)
    corpus_TFIDF = tfidf[corpus]
    
    print("---------------------시행 전 LDA 학습 시작------------------------")
    
    lda_modeling_and_visualization(corpus_TFIDF, dictionary, data_year, subject_pre)

    print("---------------------시행 후 사전 생성------------------------")

    #딕셔너리 생성 
    dictionary = Dictionary(filtered_df_second['content'])
    print("idword : ", list(dictionary.items())[:10])
    #LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
    corpus = [dictionary.doc2bow(tokens) for tokens in filtered_df_second['content']]
    #tfidf로 벡터화 적용
    tfidf = TfidfModel(corpus)
    corpus_TFIDF = tfidf[corpus]
    
    print("---------------------시행 후 LDA 학습 시작------------------------")
    
    lda_modeling_and_visualization(corpus_TFIDF, dictionary, data_year, subject_post)

if __name__ == "__main__":
    main()

