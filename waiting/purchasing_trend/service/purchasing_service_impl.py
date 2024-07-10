# File: waiting/purchasing_trend/service/purchasing_service_impl.py
from waiting.purchasing_trend.service.purchasing_service import PurchasingService
from waiting.analyses.MLanalyses import MLanalyses
import pandas as pd

class PurchasingServiceImpl(PurchasingService):
    def __init__(self):
        self.analysis_tool = MLanalyses()

    def perform_kmeans_analysis(self, file_path: str, columns: list, n_clusters: int):
        data = self.analysis_tool.load_data(file_path, columns)
        labels, centers = self.analysis_tool.run_kmeans(data, n_clusters)
        return {"labels": labels.tolist(), "centers": centers.tolist()}

    def perform_polynomial_regression(self, file_path: str, columns: list, target_column: str, degree: int):
        data = self.analysis_tool.load_data(file_path, columns + [target_column])
        coef, intercept, score = self.analysis_tool.run_polynomial_regression(data, target_column, degree)
        return {"coefficients": coef.tolist(), "intercept": intercept, "score": score}