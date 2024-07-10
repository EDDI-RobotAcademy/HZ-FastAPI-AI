import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 데이터 로드
members_df = pd.read_excel('./generated_members.xlsx')
orders_df = pd.read_excel('./generated_orders.xlsx')
returns_df = pd.read_excel('./generated_returns.xlsx')
subscriptions_df = pd.read_excel('./generated_subscriptions.xlsx')


# Label Encoding을 위한 함수
def label_encode(df):
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        label_encoders[column] = le
    return df, label_encoders


# 정규화를 위한 함수
def normalize(df):
    scaler = StandardScaler()
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df


# 데이터프레임별로 전처리 및 정규화 적용
def preprocess_and_normalize(df):
    df, label_encoders = label_encode(df)

    # 시계열 데이터 처리 (필요에 따라 조정)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df.drop(columns=['date'], inplace=True)

    # 클래스 데이터 (0, 1, 2 등)가 있다면 이를 숫자로 변환
    if 'class' in df.columns:
        df['class'] = df['class'].astype(int)

    df = normalize(df)
    return df


# 각 데이터프레임에 대해 전처리 및 정규화 수행
members_df = preprocess_and_normalize(members_df)
orders_df = preprocess_and_normalize(orders_df)
returns_df = preprocess_and_normalize(returns_df)
subscriptions_df = preprocess_and_normalize(subscriptions_df)

# 정규화된 데이터 저장
members_df.to_csv('./processed_members.csv', index=False)
orders_df.to_csv('./processed_orders.csv', index=False)
returns_df.to_csv('./processed_returns.csv', index=False)
subscriptions_df.to_csv('./processed_subscriptions.csv', index=False)

# 결과 출력
print("Members DataFrame")
print(members_df.head())
print("Orders DataFrame")
print(orders_df.head())
print("Returns DataFrame")
print(returns_df.head())
print("Subscriptions DataFrame")
print(subscriptions_df.head())
