import pandas as pd
from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel, LdaMulticore
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from ast import literal_eval
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

"""
뉴스 데이터 분석

- LDA 모델링 
- 워드 클라우드 

"""

#전처리된 뉴스 파일 가져오기 
#2020년도 : 309300건
news_df = pd.read_csv("./trendAnalysis/news_data/news_data_tokenized_2020.csv")
print(news_df.head())

#데이터 프레임의 각 행을 리스트 형태로 변환
#문자열로 저장된 리스트를 실제 리스트로 변환
news_df= news_df[:10000]
news_df['tokens'] = news_df['content'].apply(literal_eval)

print("---------------------워드 클라우드------------------------")
""""

워드 클라우드 순서
1. 단어 빈도 계산
2. 워드 클라우드 생성

"""

# 모든 토큰을 하나의 리스트로 합치기
all_tokens = [token for tokens in news_df['tokens'] for token in tokens]

# 단어 빈도 계산
word_freq = Counter(all_tokens)

# 워드 클라우드 생성
wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)

# 워드 클라우드 표시
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 워드 클라우드 이미지를 파일로 저장
wordcloud.to_file('./trendAnalysis/news_data/visualization/wordcloud_2020.png')

"""
LDA 모델링 순서

1. 각 문서에 대한 토큰화 적용
2. 사전 생성
3. 단어-문서 매트릭스 생성
4. LDA 모델 구성 및 학습
5. 중요단어 확인
"""

print("---------------------사전 생성------------------------")

#딕셔너리 생성 
dictionary = Dictionary(news_df['tokens'])
print("idword : ", list(dictionary.items())[:10])

#LDA 모델링을 위해 벡터화된 문서(코퍼스) 확인
corpus = [dictionary.doc2bow(tokens) for tokens in news_df['tokens']]

#tfidf로 벡터화 적용
tfidf = TfidfModel(corpus)
corpus_TFIDF = tfidf[corpus]

print("---------------------LDA 학습------------------------")

# LdaMulticore로 LDA 모델 학습
def lda_modeling_and_visualization():
    # LdaMulticore로 LDA 모델 학습
    num_topics = 20  # 원하는 주제 수
    lda_model = LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary, passes=15, workers=6, random_state=42)

    # 각 주제별로 중요한 단어 확인
    for idx, topic in enumerate(lda_model.print_topics(num_words=5)):
        print(f"Topic {idx}: {topic}")

    # 문서별 주제 분포 확인
    for index, topic_dist in enumerate(lda_model[corpus][:5]):
        print(f"Document {index}: {topic_dist}")

    # pyLDAvis로 시각화 준비 및 저장
    vis = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, './trendAnalysis/news_data/visualization/lda_visualization_2020.html')

if __name__ == "__main__":
    lda_modeling_and_visualization()


