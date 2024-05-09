import json
import pandas as pd
from api_manager import fetch_buzz_volume

"""
언급량 데이터 수집

"""

directory = "./trendAnalysis/buzz_data/"
keyword = "정책"
interval = "day"
date = "2024"

#API로 데이터 불려오기
all_buzz_volume = fetch_buzz_volume("2024-01-01", "2024-12-31", interval, keyword , None, None, ["사회", "경제", "생활/문화"], None)

#json 파일
# with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
#     json.dump(all_buzz_volume, file, ensure_ascii=False, indent=4) 

#csv 파일
file_name = f'buzz_{keyword}_{interval}_{date}.csv'
buzz_df = pd.DataFrame(all_buzz_volume)
buzz_df.to_csv(directory + file_name, index=False)



