import pandas as pd
import os

def merge_csv_files_simple(file_paths, output_file):
    """
    여러 CSV 파일을 하나의 DataFrame으로 병합한 후 지정된 경로에 저장합니다.

    Args:
    - file_paths (list of str): 병합할 CSV 파일 경로 리스트.
    - output_file (str): 저장할 파일의 경로.

    Returns:
    - None: 결과 파일을 직접 저장합니다.
    """
    # 모든 파일을 DataFrame으로 읽어와 리스트에 저장
    dataframes = [pd.read_csv(file) for file in file_paths]

    # DataFrame 리스트를 하나로 병합
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 출력 파일의 디렉터리가 존재하는지 확인하고, 없으면 생성
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 결과 DataFrame을 CSV 파일로 저장
    merged_df.to_csv(output_file, index=False)

    print(f"File saved as {output_file}. Merged {len(file_paths)} files.")

# 사용 예시
file_list = [
    "./youthPolicyAnalysis/news_data/data/news_정책_2023_09.csv",
    "./youthPolicyAnalysis/news_data/data/news_정책_2023_10.csv",
    "./youthPolicyAnalysis/news_data/data/news_정책_2023_11.csv",
    "./youthPolicyAnalysis/news_data/data/news_정책_2023_12.csv",
    "./youthPolicyAnalysis/news_data/data/news_정책_2024_01.csv",
    "./youthPolicyAnalysis/news_data/data/news_정책_2024_02.csv"
]

merge_csv_files_simple(file_list, "./data/news/news_merged_정책_2324.csv")
