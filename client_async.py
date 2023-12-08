import asyncio
import grpc
import chat_pb2
import chat_pb2_grpc
import threading
from queue import Queue

stream = None
sync_queue = Queue()

def loop_write():
    index = 1
    while True:
        write_to_sync_queue(f"client-{index}")
        index += 1


def write_to_sync_queue(data):
    global sync_queue
    sync_queue.put(data)

async def chat(client):
    stream = client.JoinChat()

    send_task = asyncio.create_task(send(stream))

    # Receive responses
    async for response in stream:
        print(f"Received response: {response.text}")


async def send(stream):
    global sync_queue

    while True:
        data = await asyncio.get_event_loop().run_in_executor(None, sync_queue.get)
        if data is None:
            continue
        await stream.write(chat_pb2.ChatMessage(text=data))


async def run_client():
    async with grpc.aio.insecure_channel('localhost:5501') as channel:
        client = chat_pb2_grpc.ChatStub(channel)
        await chat(client)

if __name__ == '__main__':
    t = threading.Thread(target=loop_write)
    t.start()
    asyncio.run(run_client())
    t.join()
