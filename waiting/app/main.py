import os

# import aiomysql
# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kmeans.controller.kmeans_controller import kmeansRouter

# import warnings

# warnings.filterwarnings("ignore", category=aiomysql.Warning)

# async def lifespan(app: FastAPI):
    # Startup
    # app.state.dbPool = await getMySqlPool()
    # await createTableIfNeccessary(app.state.dbPool)
    #
    # yield
    #
    # # Shutdown
    # app.state.dbPool.close()
    # await app.state.dbPool.wait_closed()

app = FastAPI() # lifespan=lifespan

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

app.include_router(kmeansRouter)

# load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.0.42:8080"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.42", port=33333)