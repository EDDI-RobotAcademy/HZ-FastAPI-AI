from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

from waiting.Faker.faker_members_info import df_members

fake = Faker('ko_KR')  # 한국어 로케일 설정
Faker.seed()  # 초기 seed 설정

orders = []

# food_id와 drink_id에 해당 가격을 매핑하는 딕셔너리
food_prices = {
    1: 23000,
    2: 21000,
    3: 20000,
    4: 23000,
    5: 22000,
    6: 25000,
    7: 24000,
    8: 26000,
    9: 27000,
    10: 28000,
    11: 29000,
    12: 30000,
    13: 31000,
    14: 32000
}

drink_prices = {
    1: 5000,
    2: 5500,
    3: 6000,
    4: 6500,
    5: 7000,
    6: 7500,
    7: 8000,
    8: 8500,
    9: 9000,
    10: 9500,
    11: 10000,
    12: 10500,
    13: 11000,
    14: 11500
}

order_id_counter = 1  # 전체 주문 ID 카운터

# 1000명의 회원에 대해 주문 정보 생성
for idx in range(1, 1001):
    num_orders = random.randint(10, 500)  # 주문 개수는 10부터 500개 사이에서 랜덤
    user_orders = 0  # 각 회원의 주문 횟수를 기록할 변수
    order_date = None  # 이전 주문 날짜를 기억할 변수
    end_date = datetime.now()  # 현재 시간을 기준으로 주문 생성을 중단할 시간 설정

    for _ in range(num_orders):
        user_orders += 1
        if order_date is None:
            order_date = fake.date_time_between(start_date='-2y', end_date=end_date)
        else:
            # 현재 시간 이전의 범위에서 랜덤한 시간 간격을 추가하여 다음 주문 날짜 생성
            time_interval = timedelta(days=random.randint(1, 30), hours=random.randint(1, 24),
                                      minutes=random.randint(1, 60))
            next_order_date = order_date + time_interval

            # 다음 주문 날짜가 현재 시간 이후면 반복 중단
            if next_order_date > end_date:
                break

            order_date = next_order_date

        food_id = random.randint(1, 14)  # 1부터 14 사이의 음식 ID 생성
        drink_id = random.randint(1, 14)  # 1부터 14 사이의 음료 ID 생성

        # 정규 분포로 수량을 생성하기 위한 과정
        # 음식과 음료의 수량 생성
        food_quantity = np.round(np.random.normal(7.5, 3)).astype(int)
        drink_quantity = np.round(np.random.normal(7.5, 3)).astype(int)

        # 1 이상 14 이하로 클리핑
        food_quantity = np.clip(food_quantity, 1, 14)
        drink_quantity = np.clip(drink_quantity, 1, 14)

        # 총 구매 금액 계산
        total_purchase_amount = (food_prices[food_id] * food_quantity) + (drink_prices[drink_id] * drink_quantity)

        order_info = {
            'order_id': order_id_counter,  # 전체 주문 ID 사용
            'user_id': df_members.loc[idx - 1, 'account_id'],  # 회원의 account_id를 사용하여 user_id 설정
            'order_date': order_date,
            'food_id': food_id,
            'food_price': food_prices[food_id],  # food_id의 가격을 지정
            'drink_id': drink_id,
            'drink_price': drink_prices[drink_id],  # drink_id의 가격을 지정
            'food_quantity': food_quantity,
            'drink_quantity': drink_quantity,
            'total_purchase_amount': total_purchase_amount,
            'age': df_members.loc[idx - 1, 'Birthyear'],
            'gender': df_members.loc[idx - 1, 'Gender'],
        }
        orders.append(order_info)
        order_id_counter += 1  # 전체 주문 ID 증가

# 주문 정보를 DataFrame으로 변환
df_orders = pd.DataFrame(orders)

# 주문 정보를 엑셀 파일로 저장
# file_path_orders = 'generated_orders.xlsx'
file_path_orders = 'generated_orders.csv'
# df_orders.to_excel(file_path_orders, index=False)
df_orders.to_csv(file_path_orders, index=False)
print(f"주문 정보가 {file_path_orders} 파일로 저장되었습니다.")