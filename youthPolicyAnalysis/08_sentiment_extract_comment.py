import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from matplotlib import font_manager, rc
from preprocessor.tokenizer import extract_pos_tag
import utils

"""
감성 예측한 결과 분석 
- 전체 결과에 해당하는 댓글 감성 원그래프 그리기
- 긍정적인 결과에 나타나는 동사 추출
- 긍정적인 결과에 나타나는 형용사 추출
- 부정적인 결과에 나타나는 동사 추출
- 부정적인 결과에 나타나는 형용사 추출
"""

# 한글 폰트 설정
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 예측한 댓글 감정 데이터 불러오기
before_predicted_comments = pd.read_csv(f"./youthPolicyAnalysis/data/comment/predicted_comments_2020.csv")
print("predicted comments : ", before_predicted_comments.shape)
after_predicted_comments = pd.read_csv(f"./youthPolicyAnalysis/data/comment/predicted_comments_2324.csv")
print("predicted comments : ", after_predicted_comments.shape)

# 분석할 컬럼만 추출 
before_comments_df = before_predicted_comments.loc[:, ["date", "contents", "predicted_emotion"]]
after_comments_df = after_predicted_comments.loc[:, ["date", "contents", "predicted_emotion"]]

# 긍정 : 행복
# 부정 : 공포, 분노, 슬픔, 혐오
positive_emotions = ['행복']
negative_emotions = ['공포', '분노', '슬픔', '혐오']

print("----------개정 전 긍/부정 비율 원 그래프로 확인 ---------------")

# 날짜 형식 변환
before_comments_df['date'] = pd.to_datetime(before_comments_df['date']).dt.strftime("%Y-%m-%d")
print(before_comments_df.head())

# 원 그래프 저장 위치
pieGraph_path = f"./youthPolicyAnalysis/img/pie_graph_2020.png"

before_comments_df['emotion'] = before_comments_df['predicted_emotion'].apply(
    lambda x: '긍정' if x in positive_emotions else ('부정' if x in negative_emotions else '중립')
)

# 긍/부정 감정 분포 
before_emotions_cnt = before_comments_df["emotion"].value_counts()
print("중립 포함 감정 분포", before_emotions_cnt)
before_emotions_cnt = before_emotions_cnt[['긍정', '부정']]
print("중립 제외 감정 분포", before_emotions_cnt)

# 원 그래프 그리기
colors = ['#0079FF', '#FF204E']
plt.figure(figsize=(8, 6))
plt.pie(before_emotions_cnt, labels=before_emotions_cnt.index, autopct='%1.1f%%', colors=colors, startangle=140)
plt.axis('equal')
plt.title('개정 전 댓글 긍/부정 비율', fontsize=20)
plt.axis('equal')
plt.savefig(pieGraph_path, dpi=300)
# plt.show()

print("----------개정 후 긍/부정 비율 원 그래프로 확인 ---------------")

# 날짜 형식 변환
after_comments_df['date'] = pd.to_datetime(after_comments_df['date']).dt.strftime("%Y-%m-%d")
print(after_comments_df.head())

# 원 그래프 저장 위치
pieGraph_path = f"./youthPolicyAnalysis/img/pie_graph_2324.png"

after_comments_df['emotion'] = after_comments_df['predicted_emotion'].apply(
    lambda x: '긍정' if x in positive_emotions else ('부정' if x in negative_emotions else '중립')
)

# 긍/부정 감정 분포 
after_emotions_cnt = after_comments_df["emotion"].value_counts()
print("중립 포함 감정 분포", after_emotions_cnt)
after_emotions_cnt = after_emotions_cnt[['긍정', '부정']]
print("중립 제외 감정 분포", after_emotions_cnt)

# 원 그래프 그리기
colors = ['#0079FF', '#FF204E']
plt.figure(figsize=(8, 6))
plt.pie(after_emotions_cnt, labels=after_emotions_cnt.index, autopct='%1.1f%%', colors=colors, startangle=140)
plt.axis('equal')
plt.title('개정 후 댓글 긍/부정 비율', fontsize=20)
plt.axis('equal')
plt.savefig(pieGraph_path, dpi=300)
# plt.show()

# 결측값 제거
before_comments_df = before_comments_df.dropna(subset=['contents'])
after_comments_df = after_comments_df.dropna(subset=['contents'])

print("----------개정 전/후 댓글 동사, 형용사 추출 시작 --------------")

# 긍정/ 부정 dataframe
before_positive_comments_df = before_comments_df[before_comments_df['emotion'] == '긍정']
print("개정 전 긍정적인 댓글 추출", before_positive_comments_df.head())
after_positive_comments_df = after_comments_df[after_comments_df['emotion'] == '긍정']
print("개정 후 긍정적인 댓글 추출", after_positive_comments_df.head())

before_negative_comments_df = before_comments_df[before_comments_df['emotion'] == '부정']
print("개정 전 부정적인 댓글 추출", before_negative_comments_df.head())
after_negative_comments_df = after_comments_df[after_comments_df['emotion'] == '부정']
print("개정 후 부정적인 댓글 추출", after_negative_comments_df.head())

print("----------개정 전/후 댓글 동사 추출--------------")
# 한글자 제외
before_positive_comments_df["verbs"] = before_positive_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_verb_tagging(x)))
after_positive_comments_df["verbs"] = after_positive_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_verb_tagging(x)))

before_negative_comments_df["verbs"] = before_negative_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_verb_tagging(x)))
after_negative_comments_df["verbs"] = after_negative_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_verb_tagging(x)))

# 긍정 공통키워드 추출
common_keywords = utils.find_common_keywords(before_positive_comments_df, after_positive_comments_df, "verbs")
before_positive_comments_df['verbs'] = before_positive_comments_df['verbs'].apply(utils.remove_keywords, args=(common_keywords,))
after_positive_comments_df['verbs'] = after_positive_comments_df['verbs'].apply(utils.remove_keywords, args=(common_keywords,))

# 파일 저장
before_positive_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/verbs_tokenizer_positive_2020.csv", index=False, encoding='utf-8-sig')
after_positive_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/verbs_tokenizer_positive_2324.csv", index=False, encoding='utf-8-sig')

# 부정 공통 키워드 추출
common_keywords = utils.find_common_keywords(before_negative_comments_df, after_negative_comments_df, "verbs")
before_negative_comments_df['verbs'] = before_negative_comments_df['verbs'].apply(utils.remove_keywords, args=(common_keywords,))
after_negative_comments_df['verbs'] = after_negative_comments_df['verbs'].apply(utils.remove_keywords, args=(common_keywords,))

# 파일 저장
before_negative_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/verbs_tokenizer_negative_2020.csv", index=False, encoding='utf-8-sig')
after_negative_comments_df[['date','verbs','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/verbs_tokenizer_negative_2324.csv", index=False, encoding='utf-8-sig')

print("----------개정 전/후 댓글 형용사 추출---------------")
# 한글자 제외
before_positive_comments_df["adj"] = before_positive_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_adjective_tagging(x)))
after_positive_comments_df["adj"] = after_positive_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_adjective_tagging(x)))

before_negative_comments_df["adj"] = before_negative_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_adjective_tagging(x)))
after_negative_comments_df["adj"] = after_negative_comments_df["contents"].apply(lambda x: utils.filter_long_words(extract_pos_tag.okt_adjective_tagging(x)))

# 긍정 형용사 공통키워드 추출
common_keywords = utils.find_common_keywords(before_positive_comments_df, after_positive_comments_df, "adj")
before_positive_comments_df['adj'] = before_positive_comments_df['adj'].apply(utils.remove_keywords, args=(common_keywords,))
after_positive_comments_df['adj'] = after_positive_comments_df['adj'].apply(utils.remove_keywords, args=(common_keywords,))

# 파일 저장
before_positive_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/adj_tokenizer_positive_2020.csv", index=False, encoding='utf-8-sig')
after_positive_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/adj_tokenizer_positive_2324.csv", index=False, encoding='utf-8-sig')

# 부정 형용사 공통키워드 추출
common_keywords = utils.find_common_keywords(before_negative_comments_df, after_negative_comments_df, "adj")
before_negative_comments_df['adj'] = before_negative_comments_df['adj'].apply(utils.remove_keywords, args=(common_keywords,))
after_negative_comments_df['adj'] = after_negative_comments_df['adj'].apply(utils.remove_keywords, args=(common_keywords,))

# 파일 저장
before_negative_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/adj_tokenizer_negative_2020.csv", index=False, encoding='utf-8-sig')
after_negative_comments_df[['date','adj','emotion']].to_csv(f"./youthPolicyAnalysis/data/comment/adj_tokenizer_negative_2324.csv", index=False, encoding='utf-8-sig')
