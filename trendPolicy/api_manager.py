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
    print(response.text)
    result = response.json()
    total_news_cnt = result['total']
    print(total_news_cnt)

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
# print(all_news_documents)


# Raw 언급량 데이터 조회 API ##############################################################
"""
    특정 키워드에서 언급량 불려오기 
"""





"""
    특정 키워드에서 반응 불려오기
"""