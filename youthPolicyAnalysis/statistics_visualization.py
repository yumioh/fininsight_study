import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from matplotlib import font_manager, rc


#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터를 DataFrame으로 생성
data = {
    "Year": ["2020", "2021", "2022", "2023"],
    "사업주 및 재직자 훈련": [2471, 2635, 3342, 3277],
    "실업자 및 취약계층 훈련": [355, 588, 513, 592],
    "인력부족분야 훈련": [ 107, 117, 103, 101],
    "직업능력개발훈련예산": [13596, 17147, 16911, 18341]
}

# 판다스 DataFrame 객체 생성
df = pd.DataFrame(data)
print(df)

# 다시 그래프 생성
fig, ax1 = plt.subplots(figsize=(10, 6))
width = 0.25  # 막대의 너비
indices = range(len(df))  # x 위치를 위한 인덱스 배열

# 막대 그래프 설정
ax1.bar(indices, df['사업주 및 재직자 훈련'], width=width, color='#12CBC4', label='사업주 및 재직자 훈련', align='center')
ax1.bar([i + width for i in indices], df['실업자 및 취약계층 훈련'], width=width, color='#FFC312', label='실업자 및 취약계층 훈련', align='center')
ax1.bar([i + width*2 for i in indices], df['인력부족분야 훈련'], width=width, color='#EA2027', label='인력부족분야 훈련', align='center')

ax1.set_ylabel('인원(천명)')
ax1.set_xticks([i + width for i in indices])
ax1.set_xticklabels(df['Year'])
ax1.set_ylim(0, 6000) 
ax1.set_yticks(range(0, 6001, 1000)) 
#ax1.set_ylim(0, max(df['사업주 및 재직자 훈련'])*1.2)  # 막대 그래프 y축 범위 조정

# 선 그래프 설정
ax2 = ax1.twinx()
ax2.plot(df['Year'], df['직업능력개발훈련예산'], 'o-', label='직업능력개발훈련예산', markersize = 5, color='#5758BB')
ax2.set_ylabel('금액 (억원)')
ax2.set_ylim(0, 20000)  # 선 그래프 y축 범위 설정
ax2.set_yticks(range(0, 20001, 5000))  # 0에서 20000까지 5000 단위로 y축 눈금 설정

# 범례 추가
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('직업능력개발훈련 실시현황 (2020-2023)')
save_path = f"./trendAnalysis/sentiment_data/visualization/job_graph.png"
plt.tight_layout()
plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
#plt.show()

# 데이터를 DataFrame으로 생성
employ_data = {
    "Year": ["2020", "2021", "2022", "2023"],
    "고용률": [42.3, 44.2, 46.6, 46.5],
    "실업률": [9.0, 7.8, 6.4, 5.9]
}

# 판다스 DataFrame 객체 생성
employ_df = pd.DataFrame(employ_data)

# 다시 그래프 생성
fig, ax1 = plt.subplots(figsize=(10, 6))
# 막대 그래프 설정
ax1.bar(employ_df['Year'], employ_df['고용률'], width=0.5, label='고용률', align='center', color='#0984e3')

ax1.set_ylabel('고용률(%)')
ax1.set_xticklabels(employ_data['Year'])
ax1.set_ylim(35, 50.0) 
ax1.set_yticks(range(35, 51, 5)) 

# 선 그래프 설정
ax2 = ax1.twinx()
ax2.plot(employ_data['Year'], employ_data['실업률'], 'o-', label='실업률', markersize = 8, linewidth=3, color='#fdcb6e')
ax2.set_ylabel('실업률(%)')
ax2.set_ylim(0, 16)  # 선 그래프 y축 범위 설정
ax2.set_yticks(range(0, 16, 2)) 

# 범례 추가
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('청년 고용률과 실업률 (2020-2023)')
save_path = f"./trendAnalysis/sentiment_data/visualization/employ_graph.png"
plt.tight_layout()
plt.savefig(save_path, dpi=300)  # dpi를 높이면 해상도가 좋아집니다
plt.show()