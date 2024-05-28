from collections import Counter
from wordcloud import WordCloud
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import matplotlib.pyplot as plt
from gensim.models import LdaMulticore


# LdaMulticore로 LDA 모델 학습
def lda_modeling_and_visualization(corpus, dictionary, year, keyword):
    num_topics = 15  # 원하는 주제 수
    lda_model = LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary, passes=10, workers=6, random_state=42)

    # 각 주제별로 중요한 단어 확인
    for idx, topic in enumerate(lda_model.print_topics(num_words=5)):
        print(f"Topic {idx}: {topic}")

    # 문서별 주제 분포 확인
    for index, topic_dist in enumerate(lda_model[corpus][:5]):
        print(f"Document {index}: {topic_dist}")

    # pyLDAvis로 시각화 준비 및 저장
    filename = f'./trendAnalysis/news_data/visualization/lda_{keyword}_{year}.html'
    vis = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, filename)


#데이터프레임으로부터 워드 클라우드를 생성하는 함수
def create_wordcloud(df, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
    # 모든 토큰을 하나의 리스트로 합치기
    all_tokens = [token for tokens in df['content'] for token in tokens]

    # 단어 빈도 계산
    word_freq = Counter(all_tokens)

    # 워드 클라우드 생성
    wordcloud = WordCloud(
        font_path=font_path, 
        width=width, 
        height=height, 
        background_color=background_color, 
        colormap = "YlGnBu",
        max_words=max_words
        ).generate_from_frequencies(word_freq)
    
    #print(plt.colormaps())

    # 워드 클라우드 이미지를 파일로 저장
    wordcloud.to_file(image_path)


def create_wordcloud2(df, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
    # 모든 토큰을 하나의 리스트로 합치기
    all_tokens = [token for tokens in df['content'] for token in tokens]

    # 단어 빈도 계산
    word_freq = Counter(all_tokens)

    # 워드 클라우드 생성
    wordcloud = WordCloud(
        font_path=font_path, 
        width=width, 
        height=height, 
        background_color=background_color, 
        colormap = "Spectral_r",
        max_words=max_words
        ).generate_from_frequencies(word_freq)
    
    #print(plt.colormaps())

    # 워드 클라우드 이미지를 파일로 저장
    wordcloud.to_file(image_path)

    #YlGnBu
    #Spectral_r
    #PuOr_r
    #YlGnBu_r
    #coolwarm
    #cool
    #gnuplot_r
    #terrain

