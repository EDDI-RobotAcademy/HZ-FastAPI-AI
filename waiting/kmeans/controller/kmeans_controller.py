# 판다스로 DataFrame 만들라고 불러옴
import pandas as pd
# FastAPI Router 쓸라고 불러옴
from fastapi import APIRouter
# 사이킷런 KMeans의 클러스터 알고리즘 모델 쓰려고 불러옴
from sklearn.cluster import KMeans
# 가짜 클러스터 데이터 만들라고 불러옴
from sklearn.datasets import make_blobs
# 수치 연산 패키지임
import numpy as np
# 랜덤값 줄려고 불러옴
import random
# 날짜하고 시간 패키지임
from datetime import datetime, timedelta
# FastAPI로 main.py에서 응답 하기 위해 import 한거임
from kmeans.controller.response_form.kmeans_cluster_response_form import KmeansClusterResponseForm
# FastAPI Router()가 API 엔드포인트 찍은거임
kmeansRouter = APIRouter()
# 라우터에 get요청 보내고 주소는 /kmeans-test 설정
@kmeansRouter.get("/kmeans-test", response_model=KmeansClusterResponseForm)
async def kmeans_cluster_analysis():
    # 회원수
    n_samples = 1000

    # 클러스터 수
    n_clusters = 10

    # 클러스터 데이터를 생성
    X, _ = make_blobs(n_samples=n_samples, centers=n_clusters, random_state=42)

    # 데이터프레임 생성
    df = pd.DataFrame({
        'accountId': range(1, n_samples + 1),
        'lastpurchasedate': [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(n_samples)],
        'periodofactivity': np.random.randint(1, 366, size=n_samples),
        'birthyear': np.random.randint(1940, 2010, size=n_samples),
        'gender': np.random.choice(['Male', 'Female'], size=n_samples)
    })

    # 30일 기준으로 구독권 구매 횟수 제한
    max_purchases = (df['periodofactivity'] / 30).astype(int)

    df['totalbasicsubscriptionpurchases'] = np.random.poisson(lam=2, size=n_samples).clip(0, max_purchases)
    df['totalstandardsubscriptionpurchases'] = np.random.poisson(lam=1, size=n_samples).clip(0, max_purchases)
    df['totalpremiumsubscriptionpurchases'] = np.random.poisson(lam=0.5, size=n_samples).clip(0, max_purchases)

    # 구독권 구매 횟수가 모두 0인 경우 하나의 구독권 구매 횟수를 최소 1로 설정
    for i in range(n_samples):
        if (df.loc[i, 'totalbasicsubscriptionpurchases'] == 0 and
                df.loc[i, 'totalstandardsubscriptionpurchases'] == 0 and
                df.loc[i, 'totalpremiumsubscriptionpurchases'] == 0):
            # totalbasicsubscriptionpurchases를 최소 1로 설정
            df.loc[i, 'totalbasicsubscriptionpurchases'] = 1

    # 총 구매 횟수 및 총 구매 금액 계산
    df['totalsubscriptionpurchases'] = (
            df['totalbasicsubscriptionpurchases'] +
            df['totalstandardsubscriptionpurchases'] +
            df['totalpremiumsubscriptionpurchases']
    )
    df['totalpurchaseamount'] = (
            df['totalbasicsubscriptionpurchases'] * 5500 +
            df['totalstandardsubscriptionpurchases'] * 13500 +
            df['totalpremiumsubscriptionpurchases'] * 17000
    )

    # 조건에 따라 고객 세그먼트 분류
    df['customer_segment'] = 'Others'  # 초기화

    # 최근 구매일이 오늘 기준 180일 이내이고 subscriptions가 있으면 'recent', 그 외에는 'past'
    df.loc[df['lastpurchasedate'] >= pd.Timestamp('2023-01-01') - pd.Timedelta(days=180), 'customer_segment'] = 'Recent'

    # totalsubscriptionpurchases가 6회 이상이면 'high', 그 외에는 'low'
    df.loc[df['totalsubscriptionpurchases'] >= 6, 'customer_segment'] = df['customer_segment'] + ' High'

    # totalpurchaseamount가 50000 이상이면 'high', 그 외에는 'low'
    df.loc[df['totalpurchaseamount'] >= 50000, 'customer_segment'] = df['customer_segment'] + ' High'

    # 데이터 확인
    print(df.head())

    # 엑셀 파일로 저장
    # df.to_excel('C:/TeamProject/SK-Networks-AI-1/HZ/HZ-Django-Backend/waiting/sample_data/controller/sample_member_data.xlsx', index=False)

    # 필요한 특성 선택
    features = ['totalsubscriptionpurchases', 'totalpurchaseamount']
    X = df[features]

    # KMeans 모델 생성 및 학습
    kmeans = KMeans(n_clusters=4, n_init=10)
    kmeans.fit(X)

    # 클러스터 할당 결과
    labels = kmeans.labels_.tolist()
    centers = kmeans.cluster_centers_.tolist()
    points = X.values.tolist()  # X.values를 사용하여 numpy array를 list로 변환

    # 클러스터 이름 설정
    cluster_names = ["VIP 고객", "최근 구매했지만 돈은 안되는 고객", "떠나버린 VIP 고객", "떠낫지만 뼈 아프지 않은 고객"]
    df['cluster'] = [cluster_names[label] for label in labels]

    print(f"points: {points}, labels: {labels}, centers: {centers}")

    return {"centers": centers, "labels": labels, "points": points, "cluster_names": cluster_names}