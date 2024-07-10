# File: waiting/analyses/MLanalyses.py
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression,LogisticRegression
import os
from sklearn.decomposition import PCA
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
        kmeans.fit(data)
        return kmeans.labels_, kmeans.cluster_centers_

    def run_polynomial_regression(self, data: pd.DataFrame, target_column: str, degree: int):
        X = data.drop(columns=[target_column])
        y = data[target_column]
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        return model.coef_, model.intercept_, model.score(X_poly, y)

    def run_pca(self, data: pd.DataFrame, n_components: int):
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(data)
        return principal_components.tolist(), pca.explained_variance_ratio_.tolist()

    def run_logistic_regression(self, data: pd.DataFrame, target_column: str):
        X = data.drop(columns=[target_column])
        y = data[target_column]
        model = LogisticRegression()
        model.fit(X, y)
        return model.coef_.tolist(), model.intercept_.tolist(), model.score(X, y)