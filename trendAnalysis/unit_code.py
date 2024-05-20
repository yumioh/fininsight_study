import pandas as pd

#파일 합치기 

csv_files = ['./trendAnalysis/news_data/news_tokenized_정책_2023.csv',
             './trendAnalysis/news_data/news_tokenized_정책_2024.csv']  # CSV 파일 이름 리스트
dataframes = []  # DataFrame들을 저장할 리스트

dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# 결과 확인
print(combined_df.head())

# 결과를 새로운 CSV 파일로 저장
combined_df.to_csv('./trendAnalysis/news_data/news_tokenized_정책_23_24.csv', index=False)

print(combined_df.shape)