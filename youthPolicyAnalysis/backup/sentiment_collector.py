import json
import pandas as pd
from api_manager import fetch_sentiment_score

"""
감정분석 데이터 수집

- 모델을 전체 뉴스 데이터에 대한 감정분석으로 진행(긍/부)
- 감정분석 데이터는 굳이 merge할 필욘 없음

"""

directory = "./trendAnalysis/sentiment_data/"
keyword = "청년"
interval = "day"
model = "all" #전체 데이터에 대한 감정분석만 
date = "all"

all_sentiment_score = fetch_sentiment_score("2020-01-01", "2024-12-31", keyword, interval, model, None, None, ["사회", "경제", "정치", "생활/문화"], None)

#json 파일
# with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
#     json.dump(all_sentiment_score, file, ensure_ascii=False, indent=4) 

#csv 파일 저장
file_name = f'sentiment_{keyword}_{interval}_{date}.csv'
sentiment_df = pd.DataFrame(all_sentiment_score)
sentiment_df.to_csv(directory + file_name, index=False)