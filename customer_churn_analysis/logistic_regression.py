from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

logisticRegressionRouter = APIRouter()


@logisticRegressionRouter.get('/lr-train')
def logisticRegressionPreprocess():
    print('logistic_regression_preprocess()')

    data = pd.read_csv(
        r'C:\TeamProject\SK-Networks-AI-1\HZ\HZ-FastAPI-AI\csv_data\generated_subscriptions.csv',
    )

    print('data.head():', data.head())
    data['target'] = data['last_login_date'].apply(
        lambda x: 1 if datetime.strptime(x, "%Y-%m-%d %H:%M:%S") >= datetime(2024, 4, 1) else 0)

    # last_login_date 컬럼 삭제
    data.drop(columns=['last_login_date'], inplace=True)

    # 특성과 타겟 분리
    X = data.drop(columns=['target', 'subscription_start_date', 'subscription_end_date'])
    y = data['target']

    y.describe()

    # 범주형 변수 처리 (예: gender, subscription_type, subscription_status, favorite_genres 등)
    le = LabelEncoder()
    X['gender'] = le.fit_transform(X['gender'])
    X['favorite_genres'] = le.fit_transform(X['favorite_genres'])

    # 학습 및 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 데이터 스케일링
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Logistic Regression 모델 학습
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    # 예측
    y_pred = model.predict(X_test_scaled)

    # 모델 성능 평가
    accuracy = accuracy_score(y_test, y_pred)
    coef = model.coef_
    intercept = model.intercept_

    # 결정 경계 생성
    x_values = np.linspace(X_train_scaled[:, 0].min(), X_train_scaled[:, 0].max(), 100)
    y_values = -(intercept + coef[0][0] * x_values) / coef[0][1]

    # JSON 응답 생성
    return JSONResponse(content={
        'accuracy': accuracy,
        'coefficients': coef.tolist(),
        'intercept': intercept.tolist(),
        'data_point': {
            'X': X_test.values.tolist(),
            'y': y_test.values.tolist()
        },
        'decision_boundary': {
            'x_values': x_values.tolist(),
            'y_values': y_values.tolist()
        }
    })
