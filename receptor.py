import pyaudio
import socket
import time

# Configurações de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Reduzindo o tamanho do chunk para diminuir latência

# Configurações do socket UDP
UDP_IP = "0.0.0.0"  # Escuta em todos os endereços IP
UDP_PORT = 5005     # Porta para escutar

# Inicializa PyAudio
audio = pyaudio.PyAudio()

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
    while True:
        data, addr = sock.recvfrom(65536)  # Aumenta o tamanho máximo de recebimento
        stream.write(data)  # Escreve no stream de áudio
        # Adiciona um pequeno atraso entre os chunks
        time.sleep(0.05)  # Atraso de 50 ms entre cada chunk (ajuste conforme necessário)
except KeyboardInterrupt:
    print("Recepção finalizada.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
