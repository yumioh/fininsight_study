# 분석 데이터 조회 API ##############################################################
# 언급량 분석 API
import requests
import json

URI = "https://inpage.ai"
# 발급 받은 토큰
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiQVBJIEtleSAtIFB1YmxpYyIsImV4cCI6MTcxNzE2NzU5OS4wfQ.Dp4m-9DwZqxHtrIc6VzIkw4TNg5gsrpXOkHQ6AW2xWc"

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
    "interval": "day",
    "token": token
}
headers = {
    "Content-type": "application/json",
    "Accept": "text/plain"
}
response = requests.post(url=f"{URI}/api/biz/v1/buzz", data=json.dumps(data), headers=headers)
result = response.json()
print("{:=^80}".format(" buzz "))
print(result)
print("="*80)