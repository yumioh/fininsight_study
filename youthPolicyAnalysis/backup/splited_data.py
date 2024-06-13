import pandas as pd

# 파일 위치 및 기타 설정
directory = './youthPolicyAnalysis/data/news/'
year = "2020"
subject = "정책"
merged_file = f'{directory}merged_{subject}_{year}.csv'

output_file = f'{directory}splited_{subject}_{year}.csv'

# 수집된 뉴스 데이터 로드
news_df = pd.read_csv(merged_file)

# inp_date 필드를 datetime 형식으로 변환
news_df['inp_date'] = pd.to_datetime(news_df['inp_date'])

# 연도와 월별로 그룹화
news_df['year_month'] = news_df['inp_date'].dt.to_period('M')

# 각 그룹을 별도의 CSV 파일로 저장
for period, group in news_df.groupby('year_month'):
    group = group.drop(columns=['year_month'])
    # 디렉토리 내에 파일을 저장
    output_file = f'{directory}merged_{subject}_{year}_{period}.csv'
    group.to_csv(output_file, index=False)
    print(f"Saved {output_file} with shape {group.shape}")

print("All monthly data files have been saved.")
