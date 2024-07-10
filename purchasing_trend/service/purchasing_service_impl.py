# File: waiting/purchasing_trend/service/purchasing_service_impl.py
from purchasing_trend.service.purchasing_service import PurchasingService
from analyses.MLanalyses import MLanalyses


class PurchasingServiceImpl(PurchasingService):
    def __init__(self, base_path: str):
        self.analysis_tool = MLanalyses(base_path)

    def perform_kmeans_analysis(self, file_name: str, columns: list, n_clusters: int):
        try:
            data = self.analysis_tool.load_data(file_name, columns)
        except ValueError as e:
            raise ValueError(f"KMeans 데이터 로딩 중 오류 발생: {e}")
        labels, centers, score = self.analysis_tool.run_kmeans(data, n_clusters)
        return {"labels": labels.tolist(), "centers": centers.tolist(), "silhouette_score": score}

    def perform_polynomial_regression(self, file_name: str, columns: list, target_column: str, degree: int):
        try:
            data = self.analysis_tool.load_data(file_name, columns + [target_column])
        except ValueError as e:
            raise ValueError(f"Polynomial Regression 데이터 로딩 중 오류 발생: {e}")
        coef, intercept, mse, r2 = self.analysis_tool.run_polynomial_regression(data, target_column, degree)
        return {"coefficients": coef.tolist(), "intercept": intercept, "mse": mse, "r2": r2}

    def perform_logistic_regression(self, file_name: str, columns: list, target_column: str, threshold: float = 0.5):
        try:
            data = self.analysis_tool.load_data(file_name, columns + [target_column])
        except ValueError as e:
            raise ValueError(f"Logistic Regression 데이터 로딩 중 오류 발생: {e}")
        coef, intercept, conf_matrix, precision, recall, f1, roc_auc = self.analysis_tool.run_logistic_regression(data, target_column, threshold)
        return {"coefficients": coef, "intercept": intercept, "confusion_matrix": conf_matrix, "precision": precision, "recall": recall, "f1_score": f1, "roc_auc_score": roc_auc}

    def perform_pca_analysis(self, file_name: str, columns: list, n_components: int):
        try:
            data = self.analysis_tool.load_data(file_name, columns)
        except ValueError as e:
            raise ValueError(f"PCA 데이터 로딩 중 오류 발생: {e}")
        principal_components, explained_variance_ratio = self.analysis_tool.run_pca(data, n_components)
        return {"principal_components": principal_components, "explained_variance_ratio": explained_variance_ratio}