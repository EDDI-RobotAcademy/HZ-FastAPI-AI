# File: waiting/analyses/MLanalyses.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression,LogisticRegression
import os
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, mean_squared_error, r2_score, confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score
import pandas as pd
import numpy as np

class MLanalyses:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def load_data(self, file_name: str, columns: list):
        file_path = os.path.join(self.base_path, file_name)
        try:
            data = pd.read_csv(file_path, usecols=columns)
        except UnicodeDecodeError as e:
            raise ValueError(f"파일 인코딩 문제: {e}")
        except Exception as e:
            raise ValueError(f"데이터 로딩 중 오류 발생: {e}")
        return data

    def run_kmeans(self, data: pd.DataFrame, n_clusters: int):
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(data)
        centers = kmeans.cluster_centers_
        score = silhouette_score(data, labels)
        data_points = data.values.tolist()  # 원래 데이터 포인트 값을 리스트로 변환
        return labels.tolist(), centers.tolist(), score, data_points

    def run_polynomial_regression(self, data: pd.DataFrame, target_column: str, degree: int):
        X = data.drop(columns=[target_column])
        y = data[target_column]
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        predictions = model.predict(X_poly)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)
        return model.coef_.tolist(), model.intercept_, mse, r2, X.values.tolist(), y.tolist()



    def run_pca(self, data: pd.DataFrame, n_components: int):
            if data is None or data.empty:
                raise ValueError("데이터가 비어 있습니다.")

            pca = PCA(n_components=n_components)
            principal_components = pca.fit_transform(data)
            explained_variance_ratio = pca.explained_variance_ratio_
            loadings = pd.DataFrame(pca.components_.T, columns=[f"PC{i + 1}" for i in range(n_components)],
                                    index=data.columns)
            return principal_components.tolist(), explained_variance_ratio.tolist(), loadings.to_dict()

    def run_logistic_regression(self, data: pd.DataFrame, target_column: str, threshold: float = 0.5):
        X = data.drop(columns=[target_column])
        y = data[target_column]

        # 연속형 라벨을 이진 라벨로 변환 (0과 1이 아닌 경우에만 변환)
        if len(np.unique(y)) > 2:
            y = (y > threshold).astype(int)

        model = LogisticRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)[:, 1]
        conf_matrix = confusion_matrix(y, predictions)
        precision = precision_score(y, predictions)
        recall = recall_score(y, predictions)
        f1 = f1_score(y, predictions)
        roc_auc = roc_auc_score(y, probabilities)
        return model.coef_.tolist(), model.intercept_.tolist(), conf_matrix.tolist(), precision, recall, f1, roc_auc, probabilities.tolist(), y.tolist()
