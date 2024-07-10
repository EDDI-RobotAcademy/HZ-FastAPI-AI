from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from waiting.Faker.faker_members_info import df_members

fake = Faker('ko_KR')  # 한국어 로케일 설정
Faker.seed()  # 초기 seed 설정

subscriptions = []

# 1000명의 회원에 대해 구독 정보 생성
for idx in range(1, 1001):
    user_id = df_members.loc[idx - 1, 'account_id']
    birthyear = df_members.loc[idx - 1, 'Birthyear']
    gender = df_members.loc[idx - 1, 'Gender']

    subscription_start_date = fake.date_time_between(start_date='-2y', end_date='now')
    subscription_type = random.randint(0, 2)  # 0: 프리미엄, 1: 스탠다드, 2: 베이식
    subscription_status = random.randint(0, 1)  # 0: 활성, 1: 취소

    # 만약 구독이 취소되었다면, 종료 날짜를 설정
    if subscription_status == 1:
        subscription_end_date = fake.date_time_between(start_date=subscription_start_date, end_date='now')
    else:
        subscription_end_date = None

    last_login_date = fake.date_time_between(start_date=subscription_start_date, end_date='now')

    # 평균 시청 시간과 총 시청 시간을 정규 분포로 생성
    average_watch_time = round(np.random.normal(2.5, 1.0), 2)  # 평균 2.5시간, 표준 편차 1시간
    total_watch_time = round(np.random.normal(100.0, 30.0), 2)  # 평균 100시간, 표준 편차 30시간

    # 값이 0보다 작으면 0으로 설정
    average_watch_time = max(0, average_watch_time)
    total_watch_time = max(0, total_watch_time)

    favorite_genres = random.choice(['액션', '범죄', 'SF', '판타지', '코미디', '스릴러', '전쟁', '스포츠', '음악', '멜로', '뮤지컬'])

    subscription_info = {
        'user_id': user_id,
        'birthyear': birthyear,
        'gender': gender,
        'subscription_start_date': subscription_start_date,
        'subscription_end_date': subscription_end_date,
        'subscription_type': subscription_type,
        'subscription_status': subscription_status,
        'last_login_date': last_login_date,
        'average_watch_time': average_watch_time,
        'total_watch_time': total_watch_time,
        'favorite_genres': favorite_genres
    }

    subscriptions.append(subscription_info)

# 구독 정보를 DataFrame으로 변환
df_subscriptions = pd.DataFrame(subscriptions)

# 구독 정보를 엑셀 파일로 저장
file_path_subscriptions = 'generated_subscriptions.xlsx'
df_subscriptions.to_excel(file_path_subscriptions, index=False)
print(f"구독 정보가 {file_path_subscriptions} 파일로 저장되었습니다.")
