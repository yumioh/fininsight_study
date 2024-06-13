import requests
import re
import json
from datetime import datetime
import pandas as pd
import time

# 파일 위치 및 기타 설정
directory = './youthPolicyAnalysis/data/news/'
year = "2324"
subject = "edu"
merged_file = f'{directory}news_url_{year}_{subject}.csv'

# 수집된 뉴스 데이터 로드
news_df = pd.read_csv(merged_file)
print("news data : ", news_df.shape)

# 필요한 정보만 포함한 DataFrame 생성
comment_df = news_df[['inp_date', 'origin_url']]

# 댓글 및 날짜 정보 저장을 위한 리스트
comments_data = []

# oid, aid 값 들고 오기 
def extract_oid_aid(article_url):
    match = re.search(r"article/(\d+)/(\d+)", article_url)
    if match:
        return match.group(1), match.group(2)
    return None, None

# json으로 comment 데이터 불러오기
def get_comments(oid, aid, page, max_retries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://n.news.naver.com/mnews/article/{oid}/{aid}'
    }
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    comments_url = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv={current_time}&_callback=jQuery33109834330291963687_1717378584985&lang=ko&country=KR&objectId=news{oid}%2C{aid}&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page={page}&initialize=true&followSize=5&userType=&useAltSort=true&replyPageSize=20&sort=FAVORITE&includeAllStatus=true&_=1717378584987"
    
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(comments_url, headers=headers, timeout=10)
            if response.status_code == 200:
                match = re.search(r'\((.*)\)', response.text)
                if match:
                    json_text = match.group(1)  # JSONP 응답에서 JSON 추출
                    comments_data = json.loads(json_text)
                    return comments_data
                else:
                    print("No JSONP data found in response.")
                    return None
            else:
                print(f"Request failed with status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            retries += 1
            time.sleep(5)  # 5초 후에 재시도
    return None

# 댓글 데이터 들고오기 
def extract_all_comments(article_url):
    oid, aid = extract_oid_aid(article_url)
    if oid and aid:
        # 첫 페이지 호출하여 전체 댓글 수 확인
        first_page_comments = get_comments(oid, aid, 1)
        if first_page_comments and first_page_comments['success']:
            total_comments = first_page_comments['result']['pageModel']['totalRows']
            if total_comments == 0:  # 전체 댓글수가 0 인경우 기사 스킵
                print(f"No comments for article {oid}, {aid}.")
                return []

            all_comments = []
            pages = (total_comments // 20) + (1 if total_comments % 20 != 0 else 0)
            for page in range(1, pages + 1):  # 기사 수가 20개 이상인 경우 페이징 처리
                comments = get_comments(oid, aid, page)
                if comments and comments['success']:
                    comment_list = comments['result']['commentList']
                    contents_list = [comment['contents'] for comment in comment_list if comment['contents'].strip() != ""]
                    all_comments.extend(contents_list)
                else:
                    print(f"Failed to get comments for page {page}.")
            return all_comments
        else:
            print("Failed to get the first page comments or no comments found.")
            return []
    else:
        print("Failed to extract oid and aid.")
        return []

# 실행
for idx, row in comment_df.iterrows():
    article_url = row["origin_url"]
    inp_date = row["inp_date"]
    all_comments = extract_all_comments(article_url)
    for comment in all_comments:
        comments_data.append({'date': inp_date, 'contents': comment, 'url': article_url})

# DataFrame 생성 및 CSV 파일로 저장
comments_df = pd.DataFrame(comments_data)
comments_df.to_csv(f'{directory}comments_{subject}_{year}.csv', index=False)
print("댓글 Shape : ", comments_df.shape)
print("댓글 Dataframe : ", comments_df.head())
