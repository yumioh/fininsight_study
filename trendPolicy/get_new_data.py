import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # 환경 변수 로드
token_key = os.getenv('API_TOKEN_KEY') #env에서 토큰키 들고 오기

URI = "https://inpage.ai" #핀인사이트 페이지 

# 발급 받은 토큰
token = token_key

# Raw 데이터 조최 API ##############################################################
# [외부 공개] 데이터 원문 조회 API

data = {
    "startDate": "2024-04-01",      # 조회 시작 날짜
    "endDate": "2024-04-30",        # 조회 종료 날짜
    "search": {
        "keyword": "청년 정책",     # 검색할 키워드
        "synonyms": [
        ],
        "filter": {
            "exOr": [
                                    #제외할 키워드
            ]
        }
    },
    "category": "",                 #카테고리 
    "category_sub": "",
    "language": "ko",
    "size": 100,                    #한번에 불려오는 기사 건수
    "from": 0,                      #페이지 처리
    "token": token
}
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}

response = requests.post(url=f"{URI}/api/biz/v1/documents", data=json.dumps(data), headers=headers)
result = response.json()

total_news_cnt = result['total'] # 총 뉴스 수
#print(result) #결과 값

all_documents = []  # 모든 문서를 저장할 리스트

for start in range(0, total_news_cnt, data['size']):
    data['from'] = start  # 시작 인덱스 업데이트

    # 업데이트된 데이터로 다시 API 요청
    response = requests.post(url=f"{URI}/api/biz/v1/documents", data=json.dumps(data), headers=headers)
    page_result = response.json()  # 페이지별 결과

    all_documents.extend(page_result['documents']) # 현재 페이지의 문서를 전체 리스트에 추가

# 모든 데이터가 수집된 후 해당하는 폴더에 저장

directory = "./trendPolicy/news_data/"
file_name = "complete_news_data.json"

with open(directory + file_name, 'w', encoding='utf-8') as file:
    json.dump(all_documents, file, ensure_ascii=False, indent=4) 
    #ensure_ascii=False : ASCII 문자만 사용할지 여부,  indent=4 : 들여쓰기


