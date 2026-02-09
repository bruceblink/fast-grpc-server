from fastapi import FastAPI
import grpc
import hello_pb2
import hello_pb2_grpc

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI + uv"}

@app.get("/hello/{name}")
async def hello(name: str):
    # 1. 创建 gRPC channel
    channel = grpc.aio.insecure_channel("127.0.0.1:50051")

    # 2. 创建 stub
    stub = hello_pb2_grpc.HelloServiceStub(channel)

    # 3. 构造请求
    request = hello_pb2.HelloRequest(name=name)

    # 4. 调用 gRPC
    response = await stub.SayHello(request)

    # 5. 关闭 channel
    await channel.close()

    return {"message": response.message}