import json
import requests
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
token_key = os.getenv('API_TOKEN_KEY')  # env에서 토큰키 들고 오기

URI = "https://inpage.ai"  # 핀인사이트 페이지 URI

# Raw 뉴스 데이터 조회 API ##############################################################
"""
주어진 키워드로 뉴스 데이터를 불러와 모든 문서를 반환하는 함수.
"""

def fetch_all_newsdata(start_date, end_date, size, keyword, synonyms=None, exOr=None, category=None, category_sub=None):

     # 선택적 인자 처리
    if synonyms is None:
        synonyms = []
    if exOr is None:
        exOr = []
    if category is None:
        category = []
    if category_sub is None:
        category_sub = []
    
    # API 요청 데이터 초기 구성
    data = {
        "startDate": start_date,  #조회 시작 날짜     
        "endDate": end_date,      #조회 종료 날짜
        "search": { 
            "keyword": keyword,   #조회할 키워드
            "synonyms": synonyms,  #동의어 
            "filter": {
                "exOr": exOr  # 제외할 키워드
            }
        },
        "category": category,  #카테고리              
        "category_sub": category_sub, #서브 카테고리
        "language": "ko",
        "size": size,         #한번에 불려올 뉴스 데이터           
        "from": 0,            #페이징 처리      
        "token": token_key
    }

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain"
    }


    # 첫 번째 API 호출로 전체 뉴스 수 파악
    response = requests.post(url=f"{URI}/api/biz/v1/documents", data=json.dumps(data), headers=headers)
    result = response.json()
    total_news_cnt = result['total']
    print("총개수 : " + str(total_news_cnt))
    
    # if response.status_code != 200:
    #     print(f"API call failed with status code: {response.status_code}")
    #     print(response.text)  # 실패 응답의 내용을 출력
    #     return None

    all_documents = []  # 모든 문서를 저장할 리스트

    # 페이징 처리하여 모든 문서 수집
    for start in range(0, total_news_cnt, size):
        data['from'] = start

        response = requests.post(url=f"{URI}/api/biz/v1/documents", data=json.dumps(data), headers=headers)
        page_result = response.json()  # 페이지별 결과
        all_documents.extend(page_result['documents']) # 현재 페이지의 문서를 전체 리스트에 추가

    return all_documents

# 함수 사용 예시
# all_news_documents = fetch_all_newsdata("2024-04-01", "2024-04-30", 100, "청년 정책")
# all_news_documents = fetch_all_newsdata("2020-03-01", "2020-03-31", 10000, "정책", None, None, ["사회", "경제",  "사회", "경제", "생활/문화"], None)
# print(all_news_documents)

# Raw 언급량 데이터 조회 API ##############################################################
"""
    특정 키워드에서 언급량 불려오기 
"""
def fetch_buzz_volume(start_date, end_date, interval, keyword, synonyms=None, exOr=None, category=None, category_sub=None):
    """
    주어진 파라미터로 언급량 데이터를 조회하고 총 합계를 계산하는 함수.
    """
    data = {
        "startDate": start_date,
        "endDate": end_date,
        "search": {
            "keyword": keyword,
            "synonyms": synonyms if synonyms else [],
            "filter": {
                "exOr": exOr if exOr else []
            }
        },
        "category": category if category else "",
        "category_sub": category_sub if category_sub else "",
        "language": "ko",
        "interval": interval,
        "token": token_key
    }

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain"
    }

    response = requests.post(url=f"{URI}/api/biz/v1/buzz", data=json.dumps(data), headers=headers)

    #총 버즈량 갯수
    if isinstance(response.json(), list):
        total_buzz = sum(item['buzz'] for item in response.json())
        print("{:=^80}".format(" Total Buzz "))
        print(f"총 언급량 :: {total_buzz} 기간 :: {start_date} ~ {end_date}")
        print("{:=^80}".format(" Total Buzz "))
    else:
        print("응답 형태가 잘못되었습니다.")

    return response.json()

# 함수 사용 예시
#data = fetch_buzz_and_calculate_total("2024-04-01", "2024-04-30", 100, "청년 정책")


# Raw 반응 데이터 조회 API ##############################################################
"""
    특정 키워드에서 반응 불려오기
"""
def fetch_sentiment_score(start_date, end_date, keyword, interval, model, synonyms=None, exOr=None, category=None, category_sub=None):
    
    # 선택적 인자 처리
    if synonyms is None:
        synonyms = []
    if exOr is None:
        exOr = []
    if category is None:
        category = []
    if category_sub is None:
        category_sub = []

    # API 요청 데이터 구성
    data = {
        "startDate": start_date,  
        "endDate": end_date,    
        "search": {
            "keyword": keyword,
            "synonyms": synonyms,
            "filter": {
                "exOr": exOr
            }
        },
        "category": category,
        "category_sub": category_sub,
        "language": "ko",
        "interval": interval, # 집계 간격 결과 day, week, month
        "model": model,  #집계 방법 all, esg, character
        "token": token_key
    }

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain"
    }

    # API 호출
    response = requests.post(url=f"{URI}/api/biz/v1/sentiment", data=json.dumps(data), headers=headers)
   
    if response.status_code == 200:
        result = response.json()
        print("{:=^80}".format(" Sentiment Analysis "))
        print(result)
        print("="*80)
    else:
        print("Failed to fetch sentiment data: HTTP", response.status_code)

    return response.json()

#data = fetch_sentiment_socre("2024-04-01", "2024-04-30","청년 정책", "day", "character")