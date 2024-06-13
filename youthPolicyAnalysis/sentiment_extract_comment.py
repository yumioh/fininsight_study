import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from matplotlib import font_manager, rc
from preprocessor.tokenizer import extract_pos_tag

"""
감성 예측한 결과 분석 
- 전체 결과에 해당하는 댓글 감성 원그래프 그리기
- 긍정적인 결과에 나타나는 동사 추출
- 긍정적인 결과에 나타나는 형용사 추출
- 부정적인 결과에 나타나는 동사 추출
- 부정적인 결과에 나타나는 형용사 추출
"""

#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


#예측한 댓글 감정 데이터 들고 오기
predicted_comments = pd.read_csv("./youthPolicyAnalysis/data/predicted_comments_2020.csv")
print("predicted comments : ", predicted_comments.shape)

#분석할 컬럼만 추출 
comments_df = predicted_comments.loc[:, ["date", "contents","predicted_emotion"]]

#날짜 형식 변환
comments_df['date'] = pd.to_datetime(comments_df['date']).dt.strftime("%Y-%m-%d")
print(comments_df.head())

print("----------모든 결과 원 그래프로 확인 ---------------")

#원그래프 저장 위치
year = 2020
pieGraph_path = f"./youthPolicyAnalysis/img/pie_graph_{year}.png"

# 긍정 : 행복
# 부정 : 공포, 분노, 슬픔, 혐오
positive_emotions = ['행복']
negative_emotions = ['공포', '분노', '슬픔', '혐오']

comments_df['emotion'] = comments_df['predicted_emotion'].apply(
    lambda x: '긍정' if x in positive_emotions else ('부정' if x in negative_emotions else '중립')
)

#긍부정 감정 분포 
emotions_cnt = comments_df["emotion"].value_counts()
print("중립 포함 감정 분포",emotions_cnt)
emotions_cnt = emotions_cnt[['긍정', '부정']]
print("중립 제외 감정 분포",emotions_cnt)

#원그래프 색상지정
colors = ['#0079FF', '#FF204E']

#원그래프 그리기
plt.figure(figsize=(8, 6))
plt.pie(emotions_cnt, labels=emotions_cnt.index, autopct='%1.1f%%', colors=colors, startangle=140)
plt.axis('equal')
plt.title(f'{2020} 댓글 긍/부정 비율', fontsize=20)
plt.axis('equal') 
plt.savefig(pieGraph_path, dpi=300)
#plt.show()

print("----------긍정적인 댓글 동사 추출---------------")

#결측값 제거
comments_df = comments_df.dropna(subset=['contents'])

negative_comments_df = comments_df[comments_df['emotion'] == '긍정']
print("부정적인 댓글 추출", negative_comments_df.shape)
print(negative_comments_df.head())

negative_comments_df["verbs"] = negative_comments_df["contents"].apply(extract_pos_tag.verb_tagging)
print(negative_comments_df.head())
negative_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/verbs_tokenizer_positive_{year}.csv",index=False, encoding='utf-8-sig')

print("----------부정적인 댓글 동사 추출---------------")
negative_comments_df = comments_df[comments_df['emotion'] == '부정']
print("부정적인 댓글 추출", negative_comments_df.shape)
print(negative_comments_df.head())

negative_comments_df["verbs"] = negative_comments_df["contents"].apply(extract_pos_tag.verb_tagging)
print(negative_comments_df.head())
negative_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/verbs_tokenizer_negative_{year}.csv",index=False, encoding='utf-8-sig')

print("----------긍정적인 댓글 형용사 추출---------------")

negative_comments_df = comments_df[comments_df['emotion'] == '긍정']
print("부정적인 댓글 추출", negative_comments_df.shape)
print(negative_comments_df.head())

negative_comments_df["adj"] = negative_comments_df["contents"].apply(extract_pos_tag.adjective_tagging)
print(negative_comments_df.head())
negative_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/adj_tokenizer_positive_{year}.csv",index=False, encoding='utf-8-sig')

print("----------부정적인 댓글 형용사 추출---------------")
negative_comments_df = comments_df[comments_df['emotion'] == '부정']
print("부정적인 댓글 추출", negative_comments_df.shape)
print(negative_comments_df.head())

negative_comments_df["adj"] = negative_comments_df["contents"].apply(extract_pos_tag.adjective_tagging)
print(negative_comments_df.head())
negative_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/adj_tokenizer_negative_{year}.csv",index=False, encoding='utf-8-sig')