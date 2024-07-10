# File: waiting/analyses/MLanalyses.py
from sklearn.cluster import KMeans
import pandas as pd

class MLanalyses:
    def load_data(self, file_path: str, columns: list):
        # XLSX 파일에서 지정된 열만 읽어옵니다.
        data = pd.read_excel(file_path, usecols=columns)
        return data

    def run_kmeans(self, data: pd.DataFrame, n_clusters: int):
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(data)
        return kmeans.labels_, kmeans.cluster_centers_
