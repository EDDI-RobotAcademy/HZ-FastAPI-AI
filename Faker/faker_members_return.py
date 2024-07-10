from faker import Faker
import pandas as pd
import random

from Faker.faker_members_info import df_members

fake = Faker('ko_KR')  # 한국어 로케일 설정
Faker.seed()  # 초기 seed 설정

returns = []



# 1000명의 회원에 대해 반품 및 환불 기록 생성
for idx in range(1, 1001):
    num_returns = random.randint(0, 3)  # 반품 및 환불 기록 개수는 0부터 20개 사이에서 랜덤
    user_returns = 0  # 각 회원의 반품 및 환불 횟수를 기록할 변수

    for _ in range(num_returns):
        user_returns += 1
        return_date = fake.date_time_between(start_date='-1y', end_date='now')  # 현재 시간 이전에서 랜덤한 날짜 선택

        returned_order_id = random.randint(1, 500)  # 회원의 주문 횟수 내에서 반품할 주문 ID 선택
        returned_food_id = random.randint(1, 14)  # 1부터 14 사이의 음식 ID 선택
        returned_drink_id = random.randint(1, 14)  # 1부터 14 사이의 음료 ID 선택

        return_quantity = random.randint(1, 10)  # 반품 수량 설정 (임의의 값)

        return_info = {
            'return_id': user_returns,  # 회원의 반품 횟수를 return_id로 사용
            'user_id': df_members.loc[idx - 1, 'account_id'],  # 회원의 account_id를 사용하여 user_id 설정
            'return_date': return_date,
            'returned_order_id': returned_order_id,
            'returned_food_id': returned_food_id,
            'returned_drink_id': returned_drink_id,
            'return_quantity': return_quantity,
        }
        returns.append(return_info)

# 반품 및 환불 기록을 DataFrame으로 변환
df_returns = pd.DataFrame(returns)

# 반품 및 환불 기록을 엑셀 파일로 저장
# file_path_returns = 'generated_returns.xlsx'
file_path_returns = '../csv_data/generated_returns.json'
# df_returns.to_excel(file_path_returns, index=False)
df_returns.to_json(file_path_returns, index=False)
print(f"반품 및 환불 기록이 {file_path_returns} 파일로 저장되었습니다.")
