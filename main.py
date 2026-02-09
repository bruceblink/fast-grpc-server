from fastapi import FastAPI
import grpc
import hello_pb2
import hello_pb2_grpc
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # FastAPI 启动时
    channel = grpc.aio.insecure_channel("127.0.0.1:50051")
    stub = hello_pb2_grpc.HelloServiceStub(channel)

    _app.state.grpc_channel = channel
    _app.state.grpc_stub = stub

    yield

    # FastAPI 关闭时
    await channel.close()


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello FastAPI + uv"}

@app.get("/hello/{name}")
async def hello(name: str):
    request = hello_pb2.HelloRequest(name=name)
    response = await app.state.grpc_stub.SayHello(request)
    return {"message": response.message}