# File: waiting/purchasing_trend/controller/purchasing_trend_controller.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from waiting.purchasing_trend.service.purchasing_service_impl import PurchasingServiceImpl
import os

class KMeansRequest(BaseModel):
    file_path: str
    columns: list
    n_clusters: int

class PolynomialRegressionRequest(BaseModel):
    file_path: str
    columns: list
    target_column: str
    degree: int

router = APIRouter()

def get_purchasing_service():
    return PurchasingServiceImpl()

@router.post("/kmeans")
def kmeans_analysis(request: KMeansRequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        # 현재 작업 디렉토리를 기준으로 파일 경로 설정
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_path, request.file_path)
        result = service.perform_kmeans_analysis(file_path, request.columns, request.n_clusters)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/polynomial_regression")
def polynomial_regression_analysis(request: PolynomialRegressionRequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        # 현재 작업 디렉토리를 기준으로 파일 경로 설정
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_path, request.file_path)
        result = service.perform_polynomial_regression(file_path, request.columns, request.target_column, request.degree)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))