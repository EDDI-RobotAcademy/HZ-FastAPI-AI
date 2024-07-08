from faker import Faker
import pandas as pd
import random
import datetime

fake = Faker('ko_KR')  # locale 설정
Faker.seed()  # 초기 seed 설정

generated_emails = set()  # 생성된 이메일을 저장할 집합
generated_nicknames = set()  # 생성된 이름을 저장할 집합

members = []

# 원하는 수의 회원 정보 생성
num_members = 100  # 예시로 100명의 회원 정보 생성

# 주문 날짜 생성 함수
def random_order_date():
    start_date = datetime.date(2022, 7, 8)
    end_date = datetime.date(2024, 7, 8)
    return fake.date_between(start_date=start_date, end_date=end_date)

# 600명의 회원은 1988년부터 2002년 사이에서 생성
for _ in range(60):
    while True:
        email = fake.free_email()
        if email not in generated_emails:
            generated_emails.add(email)
            break

    while True:
        nickname = fake.name()
        if nickname not in generated_nicknames:
            generated_nicknames.add(nickname)
            break

    gender = random.choice(['male', 'female'])
    birthyear = random.randint(1988, 2002)

    member_info = {
        'Nickname': nickname,
        'Email': email,
        'Gender': gender,
        'Birthyear': birthyear,
        'Order Date': random_order_date(),
        'Total Purchase Amount': round(random.uniform(10, 500), 2),
        'Subscription Days': random.randint(1, 365),
        'Total Orders': random.randint(1, 24),
        'Total Spent': round(random.uniform(100, 5000), 2),
        'User ID': random.randint(1, 100),
        'Food ID': random.randint(1, 14),
        'Drink ID': random.randint(1, 54),
        'Order ID': random.randint(1, 600),
        'Food Quantity': random.randint(1, 10),
        'Drink Quantity': random.randint(1, 10),
        'Subscription Level': random.choice(['프리미엄', '어드밴스드', '베이직']),
        'Support Inquiries': random.randint(0, 10),
        'Customer Satisfaction': random.randint(1, 5),
        'Return Records': random.randint(0, 5),
        'Cart Abandon Rate': round(random.uniform(0, 1), 2)
    }
    members.append(member_info)

# 나머지 40명의 회원은 1924년부터 1987년, 2003년부터 2014년 사이에서 생성
for _ in range(40):
    while True:
        email = fake.free_email()
        if email not in generated_emails:
            generated_emails.add(email)
            break

    while True:
        nickname = fake.name()
        if nickname not in generated_nicknames:
            generated_nicknames.add(nickname)
            break

    gender = random.choice(['male', 'female'])
    birthyear = random.choice([random.randint(1924, 1987), random.randint(2003, 2014)])

    member_info = {
        'Nickname': nickname,
        'Email': email,
        'Gender': gender,
        'Birthyear': birthyear,
        'Order Date': random_order_date(),
        'Total Purchase Amount': round(random.uniform(10, 500), 2),
        'Subscription Days': random.randint(1, 365),
        'Total Orders': random.randint(1, 50),
        'Total Spent': round(random.uniform(100, 5000), 2),
        'User ID': random.randint(1, 1000),
        'Food ID': random.randint(1, 100),
        'Drink ID': random.randint(1, 50),
        'Order ID': random.randint(1, 1000),
        'Food Quantity': random.randint(1, 10),
        'Drink Quantity': random.randint(1, 10),
        'Subscription Level': random.choice(['프리미엄', '어드밴스드', '베이직']),
        'Support Inquiries': random.randint(0, 10),
        'Customer Satisfaction': random.randint(1, 5),
        'Return Records': random.randint(0, 5),
        'Cart Abandon Rate': round(random.uniform(0, 1), 2)
    }
    members.append(member_info)

# 생성된 회원 정보를 DataFrame으로 변환
df = pd.DataFrame(members)

# DataFrame을 엑셀 파일로 저장
file_path = 'generated_members.xlsx'
df.to_excel(file_path, index=False)

print(f"회원 정보가 {file_path} 파일로 저장되었습니다.")