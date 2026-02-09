import asyncio
import grpc

import hello_pb2
import hello_pb2_grpc


async def main():
    # 1. 连接到 gRPC server
    channel = grpc.aio.insecure_channel("127.0.0.1:50051")

    # 2. 创建 stub（可以理解为“远程对象”）
    stub = hello_pb2_grpc.HelloServiceStub(channel)

    # 3. 构造请求
    request = hello_pb2.HelloRequest(name="kanug")

    # 4. 调用远程方法
    response = await stub.SayHello(request)

    print("client received:", response.message)

    await channel.close()


if __name__ == "__main__":
    asyncio.run(main())

    # client received: Hello, kanug
