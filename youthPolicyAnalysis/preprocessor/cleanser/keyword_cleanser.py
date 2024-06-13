import re
import os

# 여러 개의 공백을 한 개의 공백으로 줄이는 함수
def reduce_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)

#특수문자 제거 
def remove_special(text):
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", text) # 특수 문자 제거
    text = re.sub(r'[^a-zA-Z0-9\sㄱ-ㅎ가-힣]', '', text)   
    text = pattern_onlyKorean.sub('',text)
    return text

#불용어 처리할 txt 파일 불려오기
#파일이 없다면 기본 파일인 stop_word.txt로
def load_stop_words(stopwords_file):
    if not os.path.exists(stopwords_file) :
        print(f"'{stopwords_file}'을 찾을 수 없습니다. 'stop_words.txt'을 기본 파일로 사용합니다")
        # 현재 스크립트의 디렉토리를 기반으로 기본 파일 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__)) #./page-report/preprocessor/cleanser
        stopwords_file = os.path.join(base_dir, 'stop_words.txt')
    
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stop_words = [line.strip() for line in file.readlines()]
    return stop_words

#불용어 처리 함수
def remove_stop_words(tokens, stop_words):
   return [token for token in tokens if token not in stop_words and len(token) > 1]

#중첩된 리스트를 하나의 리스트로 만드는 함수
def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

#한글자 제거
def remove_single_character(tokens):
    return [token for token in tokens if len(token) > 1]

#불용어 파일 불려오기
def load_stop_words(stopwords_file):
    #파일을 찾을 수 없는 경우 default = stop_words.txt로 
    if not os.path.exists(stopwords_file):
        print(f"'{stopwords_file}'을 찾을 수 없습니다. 'stop_words.txt'을 기본 파일로 사용합니다")
        base_dir = os.path.dirname(os.path.abspath(__file__)) #./page-report/preprocessor/cleanser
        stopwords_file = os.path.join(base_dir, 'stop_words.txt')

    # 불용어 파일 읽기  
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stop_words = [line.strip() for line in file.readlines()]
    return stop_words

#불용어 제거
def process_text_with_stop_words(stopwords_file, tokens):
    #불용어 파일 불려오는 함수
    stop_words = load_stop_words(stopwords_file)
    filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
    return filtered_tokens