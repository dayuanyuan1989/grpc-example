import asyncio
import grpc
import chat_pb2
import chat_pb2_grpc

async def chat(client):
    # async with client.JoinChat() as stream:
    stream = client.JoinChat()
    # Send messages
    await stream.write(chat_pb2.ChatMessage(text="Hello"))
    await stream.write(chat_pb2.ChatMessage(text="Async"))

    # Receive responses
    async for response in stream:
        print(f"Received response: {response.text}")

async def run_client():
    async with grpc.aio.insecure_channel('localhost:5501') as channel:
        client = chat_pb2_grpc.ChatStub(channel)
        await chat(client)

if __name__ == '__main__':
    asyncio.run(run_client())
