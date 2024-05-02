import socket
import threading
import json

class Broker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.subscribers = {}  # Dicionário para armazenar os subscribers e os tópicos aos quais estão inscritos
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Broker listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        print(f"Connection from {address}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed from {address}")
                break
            message = data.decode("utf-8")
            try:
                print(message)
                message = json.loads(message)
                if message.get("type") == "subscribe":
                    subscriber_id = message.get("subscriber")
                    topics = message.get("topics")
                    for topic in topics:
                        if topic in self.subscribers:
                            self.subscribers[topic].append((subscriber_id, client_socket))  # Armazenar o socket do Subscriber junto com o ID
                        else:
                            self.subscribers[topic] = [(subscriber_id, client_socket)]
                        print(f"Subscriber {subscriber_id} subscribed to topic {topic}")
                elif message.get("type") == "publish":
                    topic = message.get("topic")
                    data = message.get("data")
                    if topic in self.subscribers:
                        for subscriber_id, subscriber_socket in self.subscribers[topic]:
                            try:
                                subscriber_socket.sendall(json.dumps({'data': data}).encode("utf-8"))
                                print(f"Message published to {topic}: {data}")
                            except ConnectionResetError:
                                print(f"Failed to send message to subscriber {subscriber_id} for topic {topic}. Removing from subscription list.")
                                self.subscribers[topic].remove((subscriber_id, subscriber_socket))
                                if not self.subscribers[topic]:
                                    del self.subscribers[topic]  # Remover o tópico se não houver mais subscribers inscritos
                    else:
                        print(f"No subscribers for topic {topic}")
            except json.JSONDecodeError:
                print("Invalid JSON received")
        client_socket.close()

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8888
    broker = Broker(HOST, PORT)
    broker.start()
