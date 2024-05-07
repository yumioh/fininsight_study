import json
import pandas as pd
from api_manager import fetch_buzz_volume


all_buzz_volume = fetch_buzz_volume("2019-01-01", "2019-12-31", "month", "청년 정책")

file_date = "_2019_01"
directory = "./trendAnalysis/buzz_data/"
file_name = "buzz_data"+file_date

#json 파일
with open(directory + file_name+ ".json", 'w', encoding='utf-8') as file:
    json.dump(all_buzz_volume, file, ensure_ascii=False, indent=4) 

#csv 파일
buzz_df = pd.DataFrame(all_buzz_volume)
buzz_df.to_csv(directory + file_name + ".csv", index=False)




