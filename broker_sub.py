import socket
import argparse
import json

class Subscriber:
    def __init__(self, host, port, topics):
        self.host = host
        self.port = port
        self.topics = topics

    def connect_to_broker(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to Broker at {self.host}:{self.port}")
            self.subscribe_to_topics()
            self.receive_messages()
        except ConnectionRefusedError:
            print("Connection to Broker refused. Make sure the Broker is running.")

    def subscribe_to_topics(self):
        subscribe_message = {
            "type": "subscribe",
            "subscriber": self.client_socket.getsockname()[1],  # Use port number as subscriber ID
            "topics": self.topics
        }
        print(self.topics)
        self.client_socket.sendall(json.dumps(subscribe_message).encode("utf-8"))

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            print(message)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Subscriber for Broker")
    parser.add_argument("-t", "--topics", nargs="+", help="Topics to subscribe to", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    HOST = "localhost"
    PORT = 8888  # Port where the Broker is running
    topics = args.topics
    subscriber = Subscriber(HOST, PORT, topics)
    subscriber.connect_to_broker()


# python3 broker_sub.py -t topic1 topic2 topic3
