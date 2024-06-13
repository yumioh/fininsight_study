import pandas as pd
from api_manager import fetch_all_newsdata

"""
뉴스 데이터 수집

"""

# 모든 데이터가 수집된 후 해당하는 폴더에 저장
directory = "./trendAnalysis/news_data/data/"
keyword = "정책"
date = "2023_11"
from_date = "2023-11-01"
to_date = "2023-11-31"

#정책 관련 데이터 수집을 위해 사회, 정치, 경제, 생활/문화 분야로 한정
all_news_data = fetch_all_newsdata(from_date, to_date, 10000, keyword, None, None, ["사회", "정치", "경제", "생활/문화"], None)

#json 파일로 만들기
# with open(directory + file_name +".json", 'w', encoding='utf-8') as file:
#     json.dump(all_news_data, file, ensure_ascii=False, indent=4) 
    #ensure_ascii=False : ASCII 문자만 사용할지 여부,  indent=4 : 들여쓰기

#csv 파일로 저장
file_name = f'news_{keyword}_{date}.csv'
news_df = pd.DataFrame(all_news_data)
news_df.to_csv(directory + file_name, index=False, encoding="utf-8-sig")

