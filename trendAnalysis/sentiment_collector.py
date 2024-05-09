import json
import pandas as pd
from api_manager import fetch_sentiment_score

"""
감정분석 데이터 수집

- 모델을 전체 뉴스 데이터에 대한 감정분석으로 진행(긍/부)

"""

model = "all" #전체 데이터에 대한 감정분석
all_sentiment_score = fetch_sentiment_score("2020-11-01", "2020-11-30","정책", "day", model, None, None, ["사회", "경제", "생활/문화"], None)

file_date = "_2020_11"
directory = "./trendAnalysis/sentiment_data/"
file_name = "sentiment_data_"+ model + file_date

#json 파일
# with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
#     json.dump(all_sentiment_score, file, ensure_ascii=False, indent=4) 

#csv 파일
sentiment_df = pd.DataFrame(all_sentiment_score)
sentiment_df.to_csv(directory + file_name + ".csv", index=False)