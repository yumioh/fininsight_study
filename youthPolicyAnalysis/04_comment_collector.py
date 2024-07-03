import requests
import re
import json
import pandas as pd

"""
네이터 뉴스 댓글 수집

- 첫 페이지에서 총 댓글 수를 파악한 후, 해당 값을 기준으로 모든 댓글을 일괄적으로 수집

"""

# 파일 위치 및 기타 설정
directory = './youthPolicyAnalysis/data/news/'
year = "2324"
subject = "policy"
merged_file = f'{directory}news_url_{year}_{subject}.csv'

# 수집된 뉴스 데이터 로드
news_df = pd.read_csv(merged_file)
print("news data : ", news_df.shape)

# 필요한 정보만 포함한 DataFrame 생성
comment_df = news_df[['inp_date', 'origin_url']][:100]

# 댓글 및 날짜 정보 저장을 위한 리스트
comments_data = []

# oid, aid 값 들고 오기
def extract_oid_aid(article_url):
    match = re.search(r"article/(\d+)/(\d+)", article_url)
    if match:
        return match.group(1), match.group(2)
    match = re.search(r"oid=(\d+)&aid=(\d+)", article_url)
    if match:
        return match.group(1), match.group(2)
    return None, None

# json으로 comment 데이터 불러오기
def get_comments(oid, aid, pageSize):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://n.news.naver.com/mnews/article/{oid}/{aid}'
    }

    comments_url = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&pool=cbox5&lang=ko&country=KR&objectId=news{oid}%2C{aid}&pageSize={pageSize}&listType=OBJECT&pageType=more&page=1&sort=FAVORITE"
    
    try:
        response = requests.get(comments_url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'\((.*)\)', response.text)
            if match:
                json_text = match.group(1)  # JSONP 응답에서 JSON 추출
                comments_data = json.loads(json_text)
                return comments_data
        print(f"Request failed with status code {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# 첫 페이지 댓글 수 가져오기
def get_total_comments(oid, aid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://n.news.naver.com/mnews/article/{oid}/{aid}'
    }

    comments_url = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&pool=cbox5&lang=ko&country=KR&objectId=news{oid}%2C{aid}&pageSize=1&listType=OBJECT&pageType=more&sort=FAVORITE"
    
    try:
        response = requests.get(comments_url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'\((.*)\)', response.text)
            if match:
                json_text = match.group(1)  # JSONP 응답에서 JSON 추출
                comments_data = json.loads(json_text)
                if comments_data['success']:
                    total_comments = comments_data['result']['pageModel']['totalRows']
                    return total_comments
        print(f"Request failed with status code {response.status_code}")
        return 0
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 0

# 댓글 데이터 들고오기
def extract_all_comments(article_url):
    oid, aid = extract_oid_aid(article_url)
    if oid and aid:
        total_comments = get_total_comments(oid, aid)
        if total_comments == 0:  # 전체 댓글수가 0인 경우 기사 스킵
            print(f"No comments for article {oid}, {aid}.")
            return []

        # 모든 댓글을 한 번에 가져오기
        comments = get_comments(oid, aid, total_comments)
        if comments and comments['success']:
            comment_list = comments['result']['commentList']
            contents_list = [comment['contents'] for comment in comment_list if comment['contents'].strip()]
            return contents_list
        print("Failed to get comments.")
        return []
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
comments_df.to_csv(f'./youthPolicyAnalysis/data/comment/comments_{subject}_{year}.csv', index=False)
print("댓글 데이터 Shape : ", comments_df.shape)
print("댓글 데이터 Dataframe : ", comments_df.head())
