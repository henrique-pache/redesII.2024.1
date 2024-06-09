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
            print(f"Conectado ao Broker em {self.host}:{self.port}")
            self.publish_message()
        except ConnectionRefusedError:
            print("Conexão ao Broker recusada.")

    def publish_message(self):
        publish_message = {
            "type": "publish",
            "topic": self.topic,
            "data": self.message
        }
        self.client_socket.sendall(json.dumps(publish_message).encode("utf-8"))
        print("Mensagem publicada com sucesso")
        self.client_socket.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Publisher for Broker")
    parser.add_argument("-t", "--topic", help="Topic to publish to", required=True)
    parser.add_argument("-m", "--message", help="Message to publish", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    HOST = "localhost"
    PORT = 8888  # Porta do Broker
    publisher = Publisher(HOST, PORT, args.topic, args.message)
    publisher.connect_to_broker()



# para publicar uma mensagem a um topico
# python broker_pub.py --topic topico --message mensagem
