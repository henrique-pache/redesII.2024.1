import socket
import threading
import json
import pyaudio
import time

class AudioServer:
    def __init__(self, broker_host, broker_port):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.subscriber_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.topics = ["MPB", "ROCK"]
        self.clients = {"MPB": [], "ROCK": []}
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=512)

    def subscribe(self):
        self.subscriber_socket.connect((self.broker_host, self.broker_port))
        message = json.dumps({"type": "subscribe", "subscriber": "audio_server", "topics": self.topics})
        self.subscriber_socket.sendall(message.encode("utf-8"))
        print(f"Subscribed to topics: {self.topics}")

    def handle_requests(self):
        while True:
            data = self.subscriber_socket.recv(1024)
            if not data:
                break
            try:
                message = json.loads(data.decode("utf-8"))
                print(f"Received message: {message}")
                if 'topic' in message and 'data' in message:
                    topic = message['topic']
                    client_address = message['data']
                    client_ip, client_port = client_address.split(":")
                    self.clients[topic].append((client_ip, int(client_port)))
                    print(f"Added client {client_ip}:{client_port} to topic {topic}")
            except json.JSONDecodeError:
                print("Invalid JSON received")

    def stream_audio(self):
        while True:
            audio_data = self.stream.read(512)
            for topic in self.topics:
                for client in self.clients[topic]:
                    self.udp_socket.sendto(audio_data, client)
                    print(f"Sent audio data to {client} for topic {topic}")

    def start(self):
        self.subscribe()
        threading.Thread(target=self.handle_requests).start()
        self.stream_audio()

if __name__ == "__main__":
    audio_server = AudioServer("localhost", 8888)
    audio_server.start()
