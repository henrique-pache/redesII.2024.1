import socket
import argparse
import json
import pyaudio
import threading
import time
from collections import deque

def parse_arguments():
    parser = argparse.ArgumentParser(description="Audio Client")
    parser.add_argument("-t", "--topic", help="Genre to subscribe to", required=True)
    parser.add_argument("-m", "--address", help="Client address in format ip:port", required=True)
    return parser.parse_args()

class AudioClient:
    def __init__(self, genre, client_address):
        self.genre = genre
        self.client_ip, self.client_port = client_address.split(':')
        self.client_port = int(self.client_port)
        self.audio_queue = deque()
        self.playing = False

    def publish_request(self, broker_host, broker_port):
        message = {
            "genre": self.genre,
            "address": f"{self.client_ip}:{self.client_port}"
        }
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((broker_host, broker_port))
        client_socket.sendall(json.dumps(message).encode('utf-8'))
        client_socket.close()

    def start_receiving(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.client_ip, self.client_port))
        threading.Thread(target=self.receive_audio, args=(udp_socket,)).start()

    def receive_audio(self, udp_socket):
        while True:
            data, _ = udp_socket.recvfrom(65536)
            self.audio_queue.append(data)
            if not self.playing:
                self.playing = True
                threading.Thread(target=self.play_audio).start()

    def play_audio(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 4096
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

        while self.playing:
            if self.audio_queue:
                chunk = self.audio_queue.popleft()
                stream.write(chunk)
            else:
                time.sleep(0.01)

        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    args = parse_arguments()
    genre = args.topic
    client_address = args.address

    client = AudioClient(genre, client_address)
    client.publish_request("localhost", 9090)
    client.start_receiving()
