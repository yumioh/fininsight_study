import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
"""
감정분석 데이터 시각화

- 굳이 파일을 merge할 필욘 없음 -> 1년치 수집 가능
- 시계열 그래프와 막대 그래프

"""
keyword = "youth_act_2020"

#청년
youth_sentiment_2020 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_청년_day_2020.csv")
youth_sentiment_2023 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_청년_day_2023.csv")
#버즈 데이터 확인
youth_sentiment_2020['date'] = pd.to_datetime(youth_sentiment_2020['date'])
youth_sentiment_2023['date'] = pd.to_datetime(youth_sentiment_2023['date'])

#정책
policy_sentiment_2020 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_정책_day_2020.csv")
policy_sentiment_2023 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_정책_day_2023.csv")
#버즈 데이터 확인
policy_sentiment_2020['date'] = pd.to_datetime(policy_sentiment_2020['date'])
policy_sentiment_2023['date'] = pd.to_datetime(policy_sentiment_2023['date'])

#청년기본법 2020 ~ 2024
youth_act_sentiment_2024 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_청년기본법_day_2024.csv")
youth_act_sentiment_2024['date'] = pd.to_datetime(youth_act_sentiment_2024['date'])

#청년기본법 2020
youth_act_sentiment_2020 = pd.read_csv("./trendAnalysis/sentiment_data/sentiment_청년기본법_day_2020.csv")
youth_act_sentiment_2020['date'] = pd.to_datetime(youth_act_sentiment_2020['date'])



print("---------------------시계열 그래프 그리기(개별적)------------------------")

save_path = f"./trendAnalysis/sentiment_data/visualization/{keyword}_sentiment_comparison.png"

plt.figure(figsize=(10, 6))
plt.bar(youth_act_sentiment_2020["date"], youth_act_sentiment_2020["score"], linestyle="-", color="blue", label="Sentiment Score")
plt.xlabel("Date")
plt.ylabel("Sentiment Score")
plt.title("Sentiment Score 2020")
plt.axhline(0, color='black', linewidth=0.5)  # 중립적인 감정 기준선
plt.grid()
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(save_path, dpi=300)
plt.show()


print("---------------------원형그래프------------------------")

save_path = f"./trendAnalysis/sentiment_data/visualization/{keyword}_sentiment_pie.png"

positive = len(youth_act_sentiment_2020[youth_act_sentiment_2024['score'] > 0])
negative = len(youth_act_sentiment_2020[youth_act_sentiment_2024['score'] < 0])
neutral = len(youth_act_sentiment_2020[youth_act_sentiment_2024['score'] == 0])

# 원형 그래프 그리기
labels = ['Positive', 'Negative', 'Neutral']
sizes = [positive, negative, neutral]
colors = ['blue', 'red', 'orange']
explode = (0.1, 0.1, 0.1)  # 각 섹션의 분리 정도

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Youth Act Sentiment Distribution 2020'")
plt.axis('equal')  # 원형 그래프를 원 모양으로 유지
plt.savefig(save_path, dpi=300)
plt.show()

print("---------------------막대 그래프 비교------------------------")

# # 막대 그래프 그리기
# plt.figure(figsize=(10, 6))
# width = 0.35  # 막대 폭

# # 2020년과 2023년 데이터프레임 가져오기
# sentiment_2020_sorted = youth_sentiment_2020.sort_values('date')
# sentiment_2023_sorted = youth_sentiment_2023.sort_values('date')

# days_2020 = range(len(sentiment_2020_sorted))
# days_2023 = range(len(sentiment_2023_sorted))

# # 각 연도 데이터의 길이 차이를 인식하며 그리기
# plt.bar(days_2020, sentiment_2020_sorted['score'], width, label="2020", color="red")
# plt.bar(days_2023, sentiment_2023_sorted['score'], width, label="2023", color="blue")

# # 날짜 레이블 설정
# plt.xticks(days_2020, [date.strftime("%m-%d") for date in sentiment_2020_sorted['date']], rotation=45)

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d")) 

# save_path = f"./trendAnalysis/sentiment_data/visualization/{keyword}_sentiment_comparison.png"

# # 레이블, 타이틀, 범례 등 추가
# plt.xlabel("Day")
# plt.ylabel("score")
# plt.title("Sentiment Score")
# plt.legend()
# plt.tight_layout()
# plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
# plt.show()

