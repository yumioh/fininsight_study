import json
import requests
from api_manager import fetch_all_newsdata

all_news_data = fetch_all_newsdata("2024-04-01", "2024-04-30", 100, "청년 정책")

# 모든 데이터가 수집된 후 해당하는 폴더에 저장
directory = "./trendPolicy/news_data/"
file_name = "complete_news_data.json"

with open(directory + file_name, 'w', encoding='utf-8') as file:
    json.dump(all_news_data, file, ensure_ascii=False, indent=4) 
    #ensure_ascii=False : ASCII 문자만 사용할지 여부,  indent=4 : 들여쓰기
