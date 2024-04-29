import socket
import argparse
import json

class Publisher:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect_to_broker(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to Broker at {self.host}:{self.port}")
            self.publish_message()
        except ConnectionRefusedError:
            print("Connection to Broker refused. Make sure the Broker is running.")

    def publish_message(self):
        topic = input("Enter topic: ")
        message = input("Enter message: ")
        publish_message = {
            "type": "publish",
            "topic": topic,
            "data": message
        }
        self.client_socket.sendall(json.dumps(publish_message).encode("utf-8"))
        print("Message published successfully")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Publisher for Broker")
    parser.add_argument("-t", "--topic", help="Topic to publish to", required=True)
    parser.add_argument("-m", "--message", help="Message to publish", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    HOST = "localhost"
    PORT = 8888  # Port where the Broker is running
    publisher = Publisher(HOST, PORT)
    publisher.connect_to_broker()


# python3 broker_pub.py -t topic_name -m "your message here"