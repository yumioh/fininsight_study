import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

"""
언급량 데이터 시각화

- 언급량 데이터는 굳이 merge할 필욘 없음 -> 1년치 수집 가능
- ㅊ

"""

keyword = "youth_act"

#청년
youth_buzz_2020 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년_day_2020.csv")
youth_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년_day_2023.csv")
#버즈 데이터 확인
youth_buzz_2020['date'] = pd.to_datetime(youth_buzz_2020['date'])
youth_buzz_2023['date'] = pd.to_datetime(youth_buzz_2023['date'])

#정책
policy_buzz_2020 = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_day_2020.csv")
policy_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_day_2023.csv")
#버즈 데이터 확인
policy_buzz_2020['date'] = pd.to_datetime(policy_buzz_2020['date'])
policy_buzz_2023['date'] = pd.to_datetime(policy_buzz_2023['date'])

#청년기본법
youth_act_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년기본법_day_2020_2023.csv")
youth_act_buzz_2023['date'] = pd.to_datetime(youth_act_buzz_2023['date'])


print("---------------------시계열 그래프 그리기(개별적)------------------------")

plt.figure(figsize=(10,8))
plt.title("Buzz Volume from 2020 to 2024 ")
plt.plot(youth_act_buzz_2023["date"], youth_act_buzz_2023["buzz"], "-", label="2020", color="red")
plt.grid()

#모든 날짜 표기 
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # 하루마다 모든 날짜에 틱을 추가합니다.
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # 날짜 형식을 지정합니다.

save_path = f"./trendAnalysis/buzz_data/visualization/{keyword}_buzz_2020.png"
plt.legend(fontsize=8)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
plt.show()

print("---------------------일별 막대 그래프 비교------------------------")

# 막대 그래프 그리기
plt.figure(figsize=(10, 5))
width = 0.35  # 막대 폭

# 2020년과 2023년 데이터프레임 가져오기
buzz_2020_sorted = policy_buzz_2020.sort_values('date')
buzz_2023_sorted = policy_buzz_2023.sort_values('date')

days_2020 = range(len(buzz_2020_sorted))
days_2023 = range(len(buzz_2023_sorted))

# 각 연도 데이터의 길이 차이를 인식하며 그리기
plt.bar(days_2020, buzz_2020_sorted['buzz'], width, label="2020", color="red")
plt.bar(days_2023, buzz_2023_sorted['buzz'], width, label="2023", color="blue")

# 날짜 레이블 설정
plt.xticks(days_2020, [date.strftime("%m-%d") for date in buzz_2020_sorted['date']], rotation=45)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d")) 

save_path = f"./trendAnalysis/buzz_data/visualization/{keyword}_buzz_comparison.png"

# 레이블, 타이틀, 범례 등 추가
plt.xlabel("Day")
plt.ylabel("Buzz Count")
plt.title("Daliy Buzz Volume")
plt.legend()
plt.tight_layout()
plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
plt.show()