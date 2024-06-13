import pandas as pd
import os
from ast import literal_eval
from dotenv import load_dotenv
from visualization.wordcloud import create_wordcloud_comment, create_wordcloud_comment2
from matplotlib import font_manager, rc

"""
추출한 데이터 기준으로 워드 클라우드 만들기 
- 긍정/부정 댓글 동사 워드 클라우드
- 긍정/부정 댓글 형용사 워드 클라우드
"""

#한글 폰트 들고 오기
load_dotenv()
path = os.getenv('font_path') 
font_path = path + "NanumBarunGothic.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

#해당 년도 설정
year = 2020
print("-------------부정적인 댓글 동사 워드 클라우드------------")
verbs_negative= pd.read_csv(f"./youthPolicyAnalysis/data/verbs_tokenizer_negative_{year}.csv")
print("부정 댓글 결측지 : ", verbs_negative.shape)
create_wordcloud_comment2(verbs_negative['verbs'], font_path, f"./youthPolicyAnalysis/img/verbs_wordcloud_negative_{year}.png")

print("-------------긍정적인 댓글 동사 워드 클라우드------------")
verbs_positive= pd.read_csv(f"./youthPolicyAnalysis/data/verbs_tokenizer_positive_{year}.csv")
print("긍정 댓글 결측지 : ", verbs_positive.shape)
create_wordcloud_comment(verbs_positive['verbs'], font_path, f"./youthPolicyAnalysis/img/verbs_wordcloud_positive_{year}.png")

print("-------------부정적인 댓글 형용사 워드 클라우드------------")

verbs_negative= pd.read_csv(f"./youthPolicyAnalysis/data/adj_tokenizer_negative_{year}.csv")
print("부정 댓글 결측지  : ", verbs_negative.shape)
create_wordcloud_comment2(verbs_negative['adj'], font_path, f"./youthPolicyAnalysis/img/adj_wordcloud_negative_{year}.png")

print("-------------긍정적인 댓글 형용사 워드 클라우드------------")

verbs_positive= pd.read_csv(f"./youthPolicyAnalysis/data/adj_tokenizer_positive_{year}.csv")
print("긍정 댓글 결측지 : ", verbs_positive.shape)
create_wordcloud_comment(verbs_positive['adj'], font_path, f"./youthPolicyAnalysis/img/adj_wordcloud_positive_{year}.png")
