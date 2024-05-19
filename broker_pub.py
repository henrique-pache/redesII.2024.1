import socket
import argparse
import json

class Publisher:
    def __init__(self, host, port, topic, message):
        self.host = host
        self.port = port
        self.topic = topic
        self.message = message

    def connect_to_broker(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to Broker at {self.host}:{self.port}")
            self.publish_message()
        except ConnectionRefusedError:
            print("Connection to Broker refused. Make sure the Broker is running.")

    def publish_message(self):
        publish_message = {
            "type": "publish",
            "topic": self.topic,
            "data": self.message
        }
        self.client_socket.sendall(json.dumps(publish_message).encode("utf-8"))
        print("Message published successfully")
        self.client_socket.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Publisher for Broker")
    parser.add_argument("-t", "--topic", help="Topic to publish to", required=True)
    parser.add_argument("-m", "--message", help="Message to publish", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    HOST = "localhost"
    PORT = 8888  # Port where the Broker is running
    publisher = Publisher(HOST, PORT, args.topic, args.message)
    publisher.connect_to_broker()
