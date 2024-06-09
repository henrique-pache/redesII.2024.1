import pyaudio
import socket
import time
from collections import deque
import threading

# Configurações de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096  # Tamanho do chunk

# Configurações do socket UDP
UDP_IP = "0.0.0.0"  # Escuta em todos os endereços IP
UDP_PORT = 5005     # Porta para escutar

# Inicializa PyAudio
audio = pyaudio.PyAudio()

# Fila para armazenar os chunks recebidos
audio_queue = deque()

# Flag para indicar se a reprodução está em andamento
playing = False

# Função para reproduzir áudio da fila
def play_audio():
    global playing
    first_chunk = True
    while True:
        if audio_queue:
            print(len(audio_queue))
            if first_chunk:
                print('Conectando ao service de Streaming...')
                time.sleep(5)
                first_chunk = False
            elif len(audio_queue) < 5:
                time.sleep(1)
            chunk = audio_queue.popleft()
            stream.write(chunk)
        else:
            # Se a fila estiver vazia, espera um curto período antes de verificar novamente
            time.sleep(0.00001)
            if not playing:
                break
    playing = False

# Thread para reprodução de áudio
audio_thread = threading.Thread(target=play_audio)

# Abre stream para reprodução de áudio
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# Inicializa o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Recebendo transmissão...")

try:
    audio_thread.start()  # Inicia a thread de reprodução de áudio
    playing = True
    while True:
        data, addr = sock.recvfrom(65536)  # Recebe os dados do chunk
        audio_queue.append(data)  # Adiciona o chunk à fila
except KeyboardInterrupt:
    print("Recepção finalizada.")
finally:
    playing = False  # Sinaliza para parar a reprodução
    audio_thread.join()  # Aguarda a finalização da thread de reprodução
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
