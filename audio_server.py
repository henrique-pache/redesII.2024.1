import socket
import threading
import json
import time
from pydub import AudioSegment

class AudioServer:
    def __init__(self, host, port, genres):
        self.host = host
        self.port = port
        self.genres = genres
        self.clients = {genre: [] for genre in genres}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Audio Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            if data:
                message = json.loads(data.decode('utf-8'))
                genre = message['genre']
                ip, port = message['address'].split(':')
                port = int(port)
                if genre in self.genres:
                    self.clients[genre].append((ip, port))
                    print(f"Cliente adicionado para o gênero {genre}: {ip}:{port}")
        finally:
            client_socket.close()

    def start(self):
        threading.Thread(target=self.accept_clients).start()
        for genre in self.genres:
            threading.Thread(target=self.stream_audio, args=(genre,)).start()

    def accept_clients(self):
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def stream_audio(self, genre):
        FILENAME = f'{genre.lower()}.mp3'  # Arquivo de áudio correspondente ao gênero
        UDP_PORT = 5005

        try:
            audio = AudioSegment.from_mp3(FILENAME)
            audio = audio.set_frame_rate(44100).set_channels(1)
            raw_audio = audio.raw_data

            duration_sec = len(audio) / 1000.0
            num_chunks = int(duration_sec * 10)
            chunk_duration = duration_sec / num_chunks

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            for i in range(num_chunks):
                start_time = i * chunk_duration
                end_time = (i + 1) * chunk_duration
                chunk = audio[int(start_time * 1000):int(end_time * 1000)].raw_data

                for client in self.clients[genre]:
                    sock.sendto(chunk, client)

                time.sleep(chunk_duration * 0.95)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 9090
    GENRES = ["ROCK", "MPB"]
    server = AudioServer(HOST, PORT, GENRES)
    server.start()
