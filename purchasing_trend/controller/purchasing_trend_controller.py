# File: waiting/purchasing_trend/controller/purchasing_trend_controller.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from purchasing_trend.service.purchasing_service_impl import PurchasingServiceImpl
import os


BASE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
class KMeansRequest(BaseModel):
    file_name: str
    columns: list
    n_clusters: int

class PolynomialRegressionRequest(BaseModel):
    file_name: str
    columns: list
    target_column: str
    degree: int

class LogisticRegressionRequest(BaseModel):
    file_name: str
    columns: list
    target_column: str

class PCARequest(BaseModel):
    file_name: str
    columns: list
    n_components: int
purchasingTrendRouter = APIRouter()

def get_purchasing_service():
    return PurchasingServiceImpl(BASE_FILE_PATH)

@purchasingTrendRouter.post("/kmeans")
def kmeans_analysis(request: KMeansRequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        result = service.perform_kmeans_analysis(request.file_name, request.columns, request.n_clusters)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@purchasingTrendRouter.post("/polynomial_regression")

def polynomial_regression_analysis(request: PolynomialRegressionRequest,
                                   service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        result = service.perform_polynomial_regression(request.file_name, request.columns, request.target_column,
                                                       request.degree)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@purchasingTrendRouter.post("/logistic_regression")
def logistic_regression_analysis(request: LogisticRegressionRequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        result = service.perform_logistic_regression(request.file_name, request.columns, request.target_column)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@purchasingTrendRouter.post("/pca")
def pca_analysis(request: PCARequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        result = service.perform_pca_analysis(request.file_name, request.columns, request.n_components)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

