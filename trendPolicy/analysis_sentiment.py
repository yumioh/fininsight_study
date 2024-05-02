import json
import pandas as pd
from api_manager import fetch_sentiment_score

all_sentiment_score = fetch_sentiment_score("2024-04-01", "2024-04-30","청년 정책", "day", "character")

file_date = "_2404"
directory = "./trendPolicy/sentiment_data/"
file_name = "sentiment_data"+file_date

#json 파일
with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
    json.dump(all_sentiment_score, file, ensure_ascii=False, indent=4) 

#csv 파일
sentiment_df = pd.DataFrame(all_sentiment_score)
sentiment_df.to_csv(directory + file_name + ".csv", index=False)