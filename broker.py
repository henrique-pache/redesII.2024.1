import socket
import threading
import json

class Broker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.topics = {}  # Dicionário para armazenar os tópicos e seus subscribers
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
                    topics = message.get("topics")
                    subscriber = message.get("subscriber")
                    for topic in topics:
                        if topic in self.topics:
                            self.topics[topic].add(subscriber)
                        else:
                            self.topics[topic] = {subscriber}
                        print(f"Subscriber {subscriber} subscribed to topic {topic}")
                elif message.get("type") == "publish":
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print(self.topics)
                    topic = message.get("topic")
                    data = message.get("data")
                    if topic in self.topics:
                        for subscriber in self.topics[topic]:
                            self.client_socket.connect((self.host, self.port))
                            self.client_socket.sendall(json.dumps({'data': data}).encode("utf-8"))
                            print(f"Message published to {topic}: {data}")
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

# python3 broker.py

# kill $(lsof -t -i:8888)