import pandas as pd

processed_news = pd.read_csv("./trendAnalysis/news_data/processed_data_2020.csv")
print(processed_news.info())