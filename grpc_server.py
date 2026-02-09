import asyncio
import grpc

import hello_pb2
import hello_pb2_grpc


# 实现 proto 里定义的服务
class HelloService(hello_pb2_grpc.HelloServiceServicer):
    async def SayHello(self, request, context):
        print("server received:", request.name)
        return hello_pb2.HelloReply(
            message=f"Hello, {request.name}"
        )


async def main():
    server = grpc.aio.server()

    # 把你的实现“注册”到 server
    hello_pb2_grpc.add_HelloServiceServicer_to_server(
        HelloService(), server
    )

    server.add_insecure_port("127.0.0.1:50051")

    await server.start()
    print("gRPC server running on 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main())
