import grpc
import chat_pb2
import chat_pb2_grpc
import asyncio
import threading
from queue import Queue
import time

sync_queue = Queue()

def loop_write():
    index = 1
    while True:
        write_to_sync_queue(f"server-{index}")
        index += 1

def write_to_sync_queue(data):
    global sync_queue
    sync_queue.put(data)


class ChatService(chat_pb2_grpc.ChatServicer):
    async def JoinChat(self, request_iterator, context: grpc.ServicerContext):
        send_task = asyncio.create_task(self.send(context))

        # Iterate over incoming messages asynchronously
        async for request in request_iterator:
            # Handle incoming messages asynchronously
            print(f"Received message: {request.text}")

    async def send(self, context):
        global sync_queue

        while True:
            data = await asyncio.get_event_loop().run_in_executor(None, sync_queue.get)
            if data is None:
                continue
            # Send a response asynchronously
            response = chat_pb2.ChatMessage(text=f"Server: Hello, {data}!")
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
    t = threading.Thread(target=loop_write)
    t.start()
    asyncio.run(serve())
    t.join()
