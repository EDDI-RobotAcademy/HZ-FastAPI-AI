# File: waiting/app/main.py
from fastapi import FastAPI
from waiting.purchasing_trend.controller.purchasing_trend_controller import router as purchasing_trend_router

app = FastAPI()

# 라우터 등록
app.include_router(purchasing_trend_router, prefix="/purchasing_trend")

# 기본 경로 테스트
@app.get("/")
def read_root():
    return {"message": "한조 fastapi 루트입니다"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=22222)
