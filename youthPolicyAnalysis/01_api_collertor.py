import pandas as pd
from crawler.page_api import api_manager

"""
뉴스 데이터 수집

"""

# 모든 데이터가 수집된 후 해당하는 폴더에 저장
directory = "./data/"
keyword = "정책"
from_date = "2023-01-01"
to_date = "2023-01-15"
#정책 관련 데이터 수집을 위해 사회, 정치, 경제, 생활/문화 분야로 한정
categories = ["사회", "정치", "경제", "생활/문화"]

#뉴스 데이터 수집 함수
all_news_data = api_manager.fetch_all_newsdata(from_date, to_date, 10000, keyword, None, None, categories, None)

#csv 파일로 저장
file_name = f'newsdata_{keyword}_{from_date}_{to_date}.csv'
news_df = pd.DataFrame(all_news_data)
news_df.to_csv(directory + file_name, index=False, encoding="utf-8-sig")

"""
언급량 데이터 수집

"""
directory = "./data/"
keyword = '정책'
from_date = "2023-01-01"
to_date = "2023-01-15"
interval = "month"
synonyms = None
categories = ["사회", "정치","경제", "생활/문화"]

#API로 데이터 불려오기
all_buzz_volume = api_manager.fetch_buzz_volume(from_date, to_date, interval, keyword , synonyms, None, categories, None)

#csv 파일
file_name = f'buzzdata_{keyword}_{interval}_{from_date}_{to_date}.csv'
buzz_df = pd.DataFrame(all_buzz_volume)
buzz_df.to_csv(directory + file_name, index=False)


"""
감정분석 데이터 수집

- 모델을 전체 뉴스 데이터에 대한 감정분석으로 진행(긍/부)
- 감정분석 데이터는 굳이 merge할 필욘 없음

"""

directory = "./data/"
keyword = "정책"
from_date = "2020-01-01"
to_date = "2023-12-31"
interval = "month"
model = "all" #전체 데이터에 대한 감정분석만 
categories = ["사회", "정치","경제", "생활/문화"]

all_sentiment_score = api_manager.fetch_sentiment_score(from_date, to_date, keyword, interval, model, None, None, categories, None)

#csv 파일 저장
file_name = f'sentidata_{keyword}_{interval}_{from_date}_{to_date}.csv'
sentiment_df = pd.DataFrame(all_sentiment_score)
sentiment_df.to_csv(directory + file_name, index=False)
