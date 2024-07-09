from fastapi import APIRouter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from datetime import datetime, timedelta, date
from faker import Faker
import random

logisticRegressionRouter = APIRouter()

@logisticRegressionRouter.get("/logistic-regression_subscription")
def logistic_regression_subscription():
    print("logistic_regression_subscription")

    # 초기 설정
    fake = Faker('ko_KR')
    Faker.seed()

    # 데이터 생성 함수
    def generate_fake_data(num_records):
        subscriptions = []
        for idx in range(1, num_records + 1):
            user_id = idx
            birthyear = fake.date_of_birth(minimum_age=18, maximum_age=70).year
            gender = random.choice(['남성', '여성'])

            subscription_start_date = fake.date_time_between(start_date='-2y', end_date='now')
            subscription_end_date = fake.date_time_between_dates(datetime_start=subscription_start_date,
                                                                 datetime_end='now')

            if subscription_end_date > datetime.now():
                subscription_status = 0  # 활성
            else:
                subscription_status = 1  # 취소

            if subscription_status == 1 and (datetime.now() - subscription_end_date).days > 100:
                churn = 0  # 이탈 고객
            else:
                churn = 1  # 이탈하지 않은 고객

            subscriptions.append({
                'user_id': user_id,
                'birthyear': birthyear,
                'gender': gender,
                'subscription_start_date': subscription_start_date,
                'subscription_end_date': subscription_end_date.date(),  # datetime.date()로 변환
                'subscription_status': subscription_status,
                'churn': churn
            })

        return pd.DataFrame(subscriptions)

    # 데이터 생성
    df_subscriptions = generate_fake_data(5000)

    # 필요한 특성 선택
    features = ['gender', 'subscription_status', 'churn']

    # 선택한 특성만 추출
    df = df_subscriptions[features]

    # 범주형 변수 처리 (더미화)
    df = pd.get_dummies(df, columns=['gender'])

    # 입력 특성(X)과 타겟 변수(y) 설정
    X = df.drop(['churn'], axis=1)
    y = df['churn']

    # 데이터 분할 (학습용 데이터와 테스트용 데이터)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 데이터 표준화 (Standardization)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 로지스틱 회귀 모델 학습
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    # 모델 평가
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # 분류 보고서 출력
    print(classification_report(y_test, y_pred))
