import os
import aiomysql
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



import warnings

from waiting.logistic_regression.controller.logistic_regression_controller import logisticRegressionRouter

warnings.filterwarnings("ignore", category=aiomysql.Warning)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

app.include_router(logisticRegressionRouter)

load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.connections = set()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.42", port=33333)