import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL 수정 함수 : 기본 뉴스 url에 comment 추가
def modify_url(original_url):
    return re.sub(r'(/article/)', r'/article/comment/', original_url)

# 파일 위치 및 기타 설정
directory = './youthPolicyAnalysis/data/news/'
year = "2023"
subject = "정책"
merged_file = f'{directory}merged_{subject}_{year}-09.csv'

# 수집된 뉴스 데이터 로드
news_df = pd.read_csv(merged_file)
print("news data : ", news_df.shape)

# 필요한 정보만 포함한 DataFrame 생성
comment_df = news_df[['inp_date', 'origin_url']]

# 댓글 및 날짜 정보 저장을 위한 리스트
comments_data = []

# 각 뉴스 기사에 대한 댓글 수집 함수
def fetch_comments(row):
    url = modify_url(row['origin_url'])
    inp_date = row['inp_date']

    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.get(url)
    sleep(5)  # JavaScript 로딩 대기

    while True:
        try:
            # WebDriverWait를 사용하여 "더보기" 버튼이 보일때까지 기다림
            more_button = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'u_cbox_btn_more'))
            )
            # 버튼이 보이면 클릭
            if more_button.is_displayed():
                driver.execute_script("arguments[0].click();", more_button)
                sleep(2)
            else:
                break
        except TimeoutException:
            # "더보기" 버튼이 더 이상 없음을 확인 (10초 동안 버튼이 나타나지 않음)
            print("더보기 버튼이 없습니다.")
            break
        except Exception as e:
            # 다른 예외 처리
            print("에러 발생 : ", e)
            break

    # BeautifulSoup를 사용하여 페이지 내용 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comment_elements = soup.select("span.u_cbox_contents")
    
    comments = []
    for element in comment_elements:
        comments.append({'inp_date': inp_date, 'comment': element.text})
    
    driver.quit()
    return comments

# ThreadPoolExecutor를 사용하여 병렬로 작업 수행
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_comments, row) for index, row in comment_df.iterrows()]
    
    for future in as_completed(futures):
        comments_data.extend(future.result())

# DataFrame 생성 및 출력
comments_df = pd.DataFrame(comments_data)
comments_df.to_csv(f'{directory}comments_{subject}_{year}_09.csv')
print("댓글 Shape : ", comments_df.shape)
print("댓글 Dataframe : ", comments_df.head())
