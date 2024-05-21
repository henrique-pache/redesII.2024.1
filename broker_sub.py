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
            print(f"Conectado ao Broker em {self.host}:{self.port}")
            self.subscribe_to_topics()
            self.receive_messages()
        except ConnectionRefusedError:
            print("Conexão ao Broker recusada.")

    def subscribe_to_topics(self):
        subscribe_message = {
            "type": "subscribe",
            "subscriber": f"{self.host}:{self.port}",
            "topics": self.topics
        }
        self.client_socket.sendall(json.dumps(subscribe_message).encode("utf-8"))

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                print("Conexão finalizada pelo Broker")
                break
            message = data.decode("utf-8")
            try:
                message = json.loads(message)
                topic = message.get('topic')
                data = message.get('data')
                print(f"Mensagem recebida: '{topic}': {data}")
            except json.JSONDecodeError:
                print("JSON inválido")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Subscriber for Broker")
    parser.add_argument("-t", "--topics", nargs="+", help="Topics to subscribe to", required=True)
    parser.add_argument("-bh", "--broker_host", type=str, help="Broker host address", required=True)
    parser.add_argument("-bp", "--broker_port", type=int, help="Broker port", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    HOST = args.broker_host
    PORT = args.broker_port
    subscriber = Subscriber(HOST, PORT, args.topics)
    subscriber.connect_to_broker()


# para inscrever um subscriber em topicos
# python broker_sub.py --broker_host localhost --broker_port 8888 --topics topico1 topico2 topicoX
