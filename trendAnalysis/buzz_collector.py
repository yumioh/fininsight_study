import json
import pandas as pd
from api_manager import fetch_buzz_volume


all_buzz_volume = fetch_buzz_volume("2020-12-01", "2020-12-31", "day", "정책", None, None, ["사회", "경제", "생활/문화"], None)

file_date = "_2020_12"
directory = "./trendAnalysis/buzz_data/"
file_name = "buzz_data"+file_date

#json 파일
# with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
#     json.dump(all_buzz_volume, file, ensure_ascii=False, indent=4) 

#csv 파일
buzz_df = pd.DataFrame(all_buzz_volume)
buzz_df.to_csv(directory + file_name + ".csv", index=False)




