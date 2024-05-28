import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from dotenv import load_dotenv
from matplotlib import font_manager, rc

"""
언급량 데이터 시각화

- 언급량 데이터는 굳이 merge할 필욘 없음 -> 1년치 수집 가능

"""
#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

keyword = "act_before_after"

#청년
youth_buzz_2020 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년_day_2020.csv")
youth_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년_day_2023.csv")
#버즈 데이터 확인
youth_buzz_2020['date'] = pd.to_datetime(youth_buzz_2020['date'])
youth_buzz_2023['date'] = pd.to_datetime(youth_buzz_2023['date'])

#정책
policy_buzz_2020 = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_month_2020.csv")
policy_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_month_2023.csv")
#버즈 데이터 확인
policy_buzz_2020['date'] = pd.to_datetime(policy_buzz_2020['date'])
policy_buzz_2023['date'] = pd.to_datetime(policy_buzz_2023['date'])

print(policy_buzz_2020.shape)
print(policy_buzz_2023.shape)

#청년기본법
youth_act_buzz_2023 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년기본법_day_2020_2023.csv")
youth_act_buzz_2023['date'] = pd.to_datetime(youth_act_buzz_2023['date'])

youth_act_buzz_20_23 = pd.read_csv("./trendAnalysis/buzz_data/buzz_청년기본법_month_20_24.csv")
youth_act_buzz_20_23['date'] = pd.to_datetime(youth_act_buzz_20_23['date'])


#청년기본법 개정 전 후 
act_buzz_before = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_month_20_before.csv")
act_buzz_before['date'] = pd.to_datetime(act_buzz_before['date'])

act_buzz_after = pd.read_csv("./trendAnalysis/buzz_data/buzz_정책_month_23_before.csv")
act_buzz_after['date'] = pd.to_datetime(act_buzz_after['date'])
print("---------------------시계열 그래프 그리기(개별적)------------------------")

# plt.figure(figsize=(10,8))
# plt.title("Buzz Volume from 2020 to 2024 ")
# plt.plot(youth_act_buzz_20_23["date"], youth_act_buzz_20_23["buzz"], "-", label="year", color="red")
# plt.grid()

# #모든 날짜 표기 
# # plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # 하루마다 모든 날짜에 틱을 추가합니다.
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # 날짜 형식을 지정합니다.

# save_path = f"./trendAnalysis/buzz_data/visualization/{keyword}_buzz_20_24.png"
# plt.legend(fontsize=8)
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
# plt.show()

print("---------------------두 막대 그래프 비교------------------------")

# # 2020년과 2023년 데이터프레임 가져오기
buzz_2020_sorted = policy_buzz_2020.sort_values('date')
buzz_2023_sorted = policy_buzz_2023.sort_values('date')

common_dates = buzz_2020_sorted[buzz_2020_sorted['date'].isin(buzz_2023_sorted['date'])]
buzz_2020_common = buzz_2020_sorted[buzz_2020_sorted['date'].isin(common_dates['date'])]
buzz_2023_common = buzz_2023_sorted[buzz_2023_sorted['date'].isin(common_dates['date'])]
print(common_dates)

plt.figure(figsize=(10, 5))
width = 0.35  # 막대 폭

# x축 위치 설정
r1 = range(len(buzz_2020_common))
r2 = [x + width for x in r1]

# 2020 데이터 막대 그래프
plt.bar(r1, buzz_2020_common['buzz'], width=width, label="2020", color="red")

# 2023 데이터 막대 그래프
plt.bar(r2, buzz_2023_common['buzz'], width=width, label="2023", color="blue")

# 날짜 레이블 설정
plt.xticks([r + width / 2 for r in range(len(buzz_2020_common))], buzz_2020_common['date'].dt.strftime("%m-%d"), rotation=45)

# 레이블, 타이틀, 범례 등 추가
plt.xlabel("Day")
plt.ylabel("Buzz Count")
plt.title("Daily Buzz Volume Comparison: 2020 vs 2023")
plt.legend()
plt.tight_layout()

# 그래프 보여주기
plt.show()
