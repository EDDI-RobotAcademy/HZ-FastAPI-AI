# File: waiting/purchasing_trend/service/purchasing_service.py
from abc import ABC, abstractmethod
import pandas as pd

class PurchasingService(ABC):
    @abstractmethod
    def perform_kmeans_analysis(self, data: pd.DataFrame, n_clusters: int):
        pass

    @abstractmethod
    def perform_polynomial_regression(self, file_path: str, columns: list, target_column: str, degree: int):
        pass