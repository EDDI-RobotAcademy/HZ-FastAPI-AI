# File: waiting/app/main.py
from fastapi import FastAPI
from waiting.purchasing_trend.controller.purchasing_trend_controller import router as purchasing_trend_router

app = FastAPI()

# 라우터 등록
app.include_router(purchasing_trend_router, prefix="")

# 기본 경로 테스트
@app.get("/")
def read_root():
    return {"message": "여긴 왜 들어오셨죠?"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=22222)
