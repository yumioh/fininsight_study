import pandas as pd
from api_manager import fetch_all_newsdata


#정책 관련 데이터 수집을 위해 사회, 경제, 생활/문화 분야로 한정
all_news_data = fetch_all_newsdata("2023-12-01", "2023-12-30", 10000, "정책", None, None, ["사회", "경제", "생활/문화"], None)

# 모든 데이터가 수집된 후 해당하는 폴더에 저장
file_date = "_2023_12"
directory = "./trendAnalysis/news_data/"
file_name = "news_data" + file_date

#json 파일로 만들기
# with open(directory + file_name +".json", 'w', encoding='utf-8') as file:
#     json.dump(all_news_data, file, ensure_ascii=False, indent=4) 
    #ensure_ascii=False : ASCII 문자만 사용할지 여부,  indent=4 : 들여쓰기

#csv 파일로 만들기 
news_df = pd.DataFrame(all_news_data)
news_df.to_csv(directory + file_name +".csv", index=False, encoding="utf-8-sig")

