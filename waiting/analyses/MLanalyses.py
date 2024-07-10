# File: waiting/analyses/MLanalyses.py
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class MLanalyses:
    def load_data(self, file_path: str, columns: list):
        # XLSX 파일에서 지정된 열만 읽어옵니다.
        data = pd.read_excel(file_path, usecols=columns)
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