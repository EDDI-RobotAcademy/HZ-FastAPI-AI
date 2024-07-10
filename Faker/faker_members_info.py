from faker import Faker
import pandas as pd
import random
import datetime

fake = Faker('ko_KR')  # locale 설정
Faker.seed()  # 초기 seed 설정

generated_emails = set()  # 생성된 이메일을 저장할 집합
generated_nicknames = set()   # 생성된 이름을 저장할 집합

members = []
orders = []

# 원하는 수의 회원 정보 생성
num_members = 1000  # 1000명의 회원 정보 생성

# account_id 초기화
account_id = 1

# 700명의 회원은 1988년부터 2002년 사이에서 생성
for _ in range(700):
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
        'account_id': account_id  # account_id 추가
    }
    members.append(member_info)
    account_id += 1  # account_id 증가

# 300명의 회원은 1924년부터 1987년, 2003년부터 2014년 사이에서 생성
for _ in range(300):
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
        'account_id': account_id
    }
    members.append(member_info)
    account_id += 1  # account_id 증가

# 생성된 회원 정보를 DataFrame으로 변환
df_members = pd.DataFrame(members)

# DataFrame을 엑셀 파일로 저장
# file_path_members = 'generated_members.xlsx'
file_path_members = '../csv_data/generated_members.csv'
# df_members.to_excel(file_path_members, index=False)
df_members.to_csv(file_path_members, index=False)

print(f"회원 정보가 {file_path_members} 파일로 저장되었습니다.")