import grpc
import chat_pb2
import chat_pb2_grpc
import asyncio

class ChatService(chat_pb2_grpc.ChatServicer):
    async def JoinChat(self, request_iterator, context: grpc.ServicerContext):
        # Iterate over incoming messages asynchronously
        async for request in request_iterator:
            # Handle incoming messages asynchronously
            print(f"Received message: {request.text}")

            # Send a response asynchronously
            response = chat_pb2.ChatMessage(text=f"Server: Hello, {request.text}!")
            await self.send_message_to_client(response, context)

    async def send_message_to_client(self, message, context: grpc.ServicerContext):
        await asyncio.sleep(0.2)  # Simulate some processing time
        await context.write(message)

async def serve():
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:5501')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
