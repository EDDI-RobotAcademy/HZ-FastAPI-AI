import asyncio
import json
import os

import aiomysql
import pandas as pd
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from pydantic import BaseModel

from purchasing_trend.controller.purchasing_trend_controller import purchasingTrendRouter




async def create_kafka_topics():
    adminClient = AIOKafkaAdminClient(
        bootstrap_servers='localhost:9092',
        loop=asyncio.get_running_loop()
    )

    try:
        await adminClient.start()

        topics = [
            NewTopic(
                "test-topic",
                num_partitions=1,
                replication_factor=1,
            ),
            NewTopic(
                "completion-topic",
                num_partitions=1,
                replication_factor=1,
            ),
        ]

        for topic in topics:
            try:
                await adminClient.create_topics([topic])
            except TopicAlreadyExistsError:
                print(f"Topic '{topic.name}' already exists, skipping creation")

    except Exception as e:
        print(f"카프카 토픽 생성 실패: {e}")
    finally:
        await adminClient.close()




import warnings

warnings.filterwarnings("ignore", category=aiomysql.Warning)


async def lifespan(app: FastAPI):
    # Startup
    # app.state.dbPool = await getMySqlPool()
    # await createTableIfNeccessary(app.state.dbPool)

    # 비동기 I/O 정지 이벤트 감지
    app.state.stop_event = asyncio.Event()

    # Kafka Producer (생산자) 구성
    app.state.kafka_producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        client_id='fastapi-kafka-producer'
    )

    # Kafka Consumer (소비자) 구성
    app.state.kafka_consumer = AIOKafkaConsumer(
        'completion_topic',
        bootstrap_servers='localhost:9092',
        group_id="my_group",
        client_id='fastapi-kafka-consumer'
    )

    # 자동 생성했던 test-topic 관련 소비자
    app.state.kafka_test_topic_consumer = AIOKafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        group_id="another_group",
        client_id='fastapi-kafka-consumer'
    )

    await app.state.kafka_producer.start()
    await app.state.kafka_consumer.start()
    await app.state.kafka_test_topic_consumer.start()

    # asyncio.create_task(consume(app))
    asyncio.create_task(testTopicConsume(app))

    try:
        yield
    finally:
        # Shutdown
        # app.state.dbPool.close()
        # await app.state.dbPool.wait_closed()

        app.state.stop_event.set()

        await app.state.kafka_producer.stop()
        await app.state.kafka_consumer.stop()
        await app.state.kafka_test_topic_consumer.stop()


app = FastAPI(lifespan=lifespan)



@app.get("/")
def read_root():
    return {"message": "한조 fastapi 루트입니다"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


app.include_router(purchasingTrendRouter, prefix='/purchasing_trend')


async def testTopicConsume(app: FastAPI):
    consumer = app.state.kafka_test_topic_consumer

    while not app.state.stop_event.is_set():
        try:
            msg = await consumer.getone()
            print(f"msg: {msg}")
            data = json.loads(msg.value.decode("utf-8"))
            print(f"request data: {data}")

            # 실제로 여기서 뭔가 요청을 하던 뭘 하던 지지고 볶으면 됨
            await asyncio.sleep(60)

            for connection in app.state.connections:
                await connection.send_json({
                    'message': 'Processing completed.',
                    'data': data,
                    'title': "Kafka Test"
                })

        except asyncio.CancelledError:
            print("소비자 태스크 종료")
            break

        except Exception as e:
            print(f"소비 중 에러 발생: {e}")


load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
csv_file_path = os.getenv('CSV_FILE_PATH')

def read_csv_data(data_path):
    if csv_file_path:
        return pd.read_csv(csv_file_path + '/' + data_path)
    else:
        raise FileNotFoundError('CSV 파일 경로가 잘못되었습니다!')

@app.get('/csv-data')
async def get_csv_data(data_path):
    data = read_csv_data(data_path)
    return data#.to_dict(orient='records')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.connections = set()


class KafkaRequest(BaseModel):
    message: str


@app.post("/kafka-endpoint")
async def kafka_endpoint(request: KafkaRequest):
    eventData = request.dict()
    await app.state.kafka_producer.send_and_wait("test-topic", json.dumps(eventData).encode())

    return {"status": "processing"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.state.connections.add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        app.state.connections.remove(websocket)


if __name__ == "__main__":
    import uvicorn

    asyncio.run(create_kafka_topics())
    uvicorn.run("app.main:app", host="localhost", port=33333, reload=True)