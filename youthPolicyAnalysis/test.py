import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from matplotlib import font_manager, rc
import os

#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터 읽기
data_2020 = {
    'date': ["2020-01-01", "2020-02-01", "2020-03-01", "2020-04-01", "2020-05-01", "2020-06-01",
             "2020-07-01", "2020-08-01", "2020-09-01", "2020-10-01", "2020-11-01", "2020-12-01"],
    'buzz': [10446, 8246, 8599, 8345, 8228, 10099, 10456, 8275, 10674, 8936, 9351, 10123]
}
data_2023 = {
    'date': ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01",
             "2023-07-01", "2023-08-01", "2023-09-01", "2023-10-01", "2023-11-01", "2023-12-01"],
    'buzz': [12157, 13402, 15792, 13544, 14456, 14417, 11978, 11972, 12407, 12767, 16836, 14892]
}

policy_buzz_2020 = pd.DataFrame(data_2020)
policy_buzz_2023 = pd.DataFrame(data_2023)

# 날짜 형식 변환
policy_buzz_2020['date'] = pd.to_datetime(policy_buzz_2020['date'])
policy_buzz_2023['date'] = pd.to_datetime(policy_buzz_2023['date'])

# 월만 추출
policy_buzz_2020['month'] = policy_buzz_2020['date'].dt.month
policy_buzz_2023['month'] = policy_buzz_2023['date'].dt.month

# 막대 그래프 그리기
plt.figure(figsize=(14, 8))

# 2020 데이터 선 그래프
plt.plot(policy_buzz_2020['month'], policy_buzz_2020['buzz'], label='개정전', color='red', marker='o')

# 2023 데이터 선 그래프
plt.plot(policy_buzz_2023['month'], policy_buzz_2023['buzz'], label='개정후', color='blue', marker='o')

# 레이블, 타이틀, 범례 등 추가
plt.xlabel("Month")
plt.ylabel("Buzz Volume")
plt.title("Monthly Buzz Volume Comparison: 개정 전 vs 개정 후")
plt.legend()
plt.grid(True)
plt.xticks(range(1, 13), ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'], rotation=45)
plt.tight_layout()

# 그래프 보여주기
plt.show()
