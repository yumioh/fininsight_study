import json
import requests

# 설정 ###########################################################################

URI = "https://inpage.ai"

# 발급 받은 토큰
token = ""

# Raw 데이터 조최 API ##############################################################
# [외부 공개] 데이터 원문 조회 API
data = {
    "startDate": "2024-04-01",      # 필수
    "endDate": "2024-04-30",        # 필수 
    "search": {
        "keyword": "삼성전자",        # 필수
        "synonyms": [
            "HBM",
            "뉴삼성"
        ],
        "filter": {
            "exOr": [
                "하이닉스"
            ]
        }
    },
    "category": ["경제", "IT/과학"],
    "category_sub": ["금융", "산업/재계", "글로벌 경제", "IT 일반", "컴퓨터"],
    "language": "ko",
    "size": 100,
    "from": 0,
    "token": token
}
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}
response = requests.post(url=f"{URI}/api/biz/v1/documents", data=json.dumps(data), headers=headers)
result = response.json()
print("{:=^80}".format(" documents "))
print(result)
print("="*80)