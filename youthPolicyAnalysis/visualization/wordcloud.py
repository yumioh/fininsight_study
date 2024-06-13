from collections import Counter
from wordcloud import WordCloud


#데이터프레임으로부터 워드 클라우드를 생성하는 함수
def create_wordcloud(tokens_column, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
    # 모든 토큰을 하나의 리스트로 합치기
    #all_tokens = [token for tokens in df['content'] for token in tokens]
    all_tokens = [token for tokens in tokens_column for token in eval(tokens)]

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


def create_wordcloud2(tokens_column, font_path, image_path, width=800, height=400, background_color='white', max_words=60):
    # 모든 토큰을 하나의 리스트로 합치기
    #all_tokens = [token for tokens in df['content'] for token in tokens]
    all_tokens = [token for tokens in tokens_column for token in eval(tokens)]

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

