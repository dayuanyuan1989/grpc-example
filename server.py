import grpc
import chat_pb2
import chat_pb2_grpc
from concurrent import futures

class ChatService(chat_pb2_grpc.ChatServicer):
    def JoinChat(self, request_iterator, context: grpc.ServicerContext):
        for request in request_iterator:
            # Handle incoming messages
            print(f"Received message: {request.text}")

            # Send a response
            response = chat_pb2.ChatMessage(text=f"Server: Hello, {request.text}!")
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:5501')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

