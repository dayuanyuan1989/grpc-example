import grpc
import chat_pb2
import chat_pb2_grpc
import time

def run():
    channel = grpc.insecure_channel('localhost:5501')
    stub = chat_pb2_grpc.ChatStub(channel)

    messages = [
        chat_pb2.ChatMessage(text="Hello"),
        chat_pb2.ChatMessage(text="World"),
    ]

    responses = stub.JoinChat(iter(messages))
    while True:
        for response in responses:
            print(f"type={type(response)}")
            print(f"Received message: {response.text}")
        else:
            time.sleep(0.2)

if __name__ == '__main__':
    run()
