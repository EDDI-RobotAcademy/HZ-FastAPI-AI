from faker import Faker
import pandas as pd
from datetime import datetime, timedelta, date
import random

fake = Faker('ko_KR')  # 한국어 로케일 설정
Faker.seed()  # 초기 seed 설정

subscriptions = []

# 5000명의 회원에 대해 구독 정보 생성
for idx in range(1, 5001):
    # 회원 정보 가져오기
    user_id = idx
    birthyear = fake.date_of_birth(minimum_age=18, maximum_age=70).year
    gender = random.choice(['남성', '여성'])

    # 구독 시작일 생성 (과거 2년 이내 무작위 날짜)
    subscription_start_date = fake.date_time_between(start_date='-2y', end_date='now')

    # 구독 종료일 생성 (구독 시작일 이후의 무작위 날짜)
    subscription_end_date = fake.date_time_between_dates(datetime_start=subscription_start_date, datetime_end='now')

    # subscription_status 정의 (구독 종료일이 지금 날짜보다 이후이면 활성, 아니면 취소)
    if subscription_end_date > datetime.now():
        subscription_status = 0  # 활성
    else:
        subscription_status = 1  # 취소

    # 고객 이탈 여부 정의
    # subscription_status가 1(취소)이고, subscription_end_date가 오늘 날짜로부터 100일 이상 지났으면 이탈 고객으로 간주
    if subscription_status == 1 and (datetime.now() - subscription_end_date).days > 100:
        churn = 0  # 이탈 고객
    else:
        churn = 1  # 이탈하지 않은 고객

    subscription_info = {
        'user_id': user_id,
        'birthyear': birthyear,
        'gender': gender,
        'subscription_start_date': subscription_start_date,
        'subscription_end_date': subscription_end_date.date(),  # datetime.date()로 변환
        'subscription_status': subscription_status,
        'churn': churn
    }

    subscriptions.append(subscription_info)

# 구독 정보를 DataFrame으로 변환
df_subscriptions = pd.DataFrame(subscriptions)

# 구독 정보를 엑셀 파일로 저장
file_path_subscriptions = 'generated_subscriptions.xlsx'
df_subscriptions.to_excel(file_path_subscriptions, index=False)
print(f"구독 정보가 {file_path_subscriptions} 파일로 저장되었습니다.")