import pandas as pd

# CSV 파일 읽기
news_df = pd.read_csv("./trendAnalysis/news_data/news_tokenized_정책_23_24.csv", parse_dates=['date'])
print(news_df.shape)

# 필터링할 날짜 범위 정의
start_date = pd.Timestamp('2023-06-24')
end_date = pd.Timestamp('2023-12-20')

# 지정된 날짜 범위에 해당하는 데이터만 필터링
filtered_df = news_df[(news_df['date'] >= start_date) & (news_df['date'] <= end_date)]

# 필터링된 데이터를 새로운 CSV 파일로 저장
filtered_df.to_csv("./trendAnalysis/news_data/news_tokenized_정책_23_24_filter_1.csv", index=False)
print(filtered_df.shape)
print(filtered_df.head())