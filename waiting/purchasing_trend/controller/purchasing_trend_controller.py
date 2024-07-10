# File: waiting/purchasing_trend/controller/purchasing_trend_controller.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from waiting.purchasing_trend.service.purchasing_service_impl import PurchasingServiceImpl

class KMeansRequest(BaseModel):
    file_path: str
    columns: list
    n_clusters: int

router = APIRouter()

def get_purchasing_service():
    return PurchasingServiceImpl()

@router.post("/kmeans")
def kmeans_analysis(request: KMeansRequest, service: PurchasingServiceImpl = Depends(get_purchasing_service)):
    try:
        result = service.perform_kmeans_analysis(request.file_path, request.columns, request.n_clusters)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
