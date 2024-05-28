import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
# 나눔고딕 폰트 경로 (예시: Windows의 경우) 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

act_keyword_before = pd.read_csv("./trendAnalysis/news_data/keyword_act_before.csv")
act_keyword_after = pd.read_csv("./trendAnalysis/news_data/keyword_act_after.csv")

# print(act_keyword_before.head())
# print(act_keyword_after.head())

# 데이터프레임의 첫 몇 행 출력
print(act_keyword_before.head())
print(act_keyword_after.head())


# plt.figure(figsize=(12, 8))
# plt.bar(act_keyword_before['키워드'][:10], act_keyword_before['키워드수'][:10], color='blue')
# plt.xlabel('키워드')
# plt.ylabel('키워드 수')
# plt.title('청년 기본법 개정 전 키워드별 빈도수')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()

#교육 : FFC312 일자리 : EA2027 창업 : 12CBC4 고용 : FDA7DF 취업 ED4C67 복지 cbe86b 여성  80d4f6 인구 00dffc 공공 1289A7 주택 D980FA
 
colors = ['#FFC312','#EA2027','#12CBC4','#FDA7DF','#ED4C67','#cbe86b', '#e4e7ec','#00dffc','#1289A7','#D980FA']
af_colors = ['#FFC312', '#00dffc','#EA2027','#cbe86b','#ED4C67','#5c196b','#fec8c9','#12CBC4','#EE5A24','#e4e7ec']

# 원 그래프 그리기 (개정 후)
plt.figure(figsize=(10, 10))
plt.pie(act_keyword_after['키워드수'][:10], labels=act_keyword_after['키워드'][:10], autopct='%1.1f%%', startangle=140, colors=af_colors)
plt.title('청년 기본법 개정 후 주요 키워드 빈도수', y=1.08)
plt.axis('equal')
plt.show()