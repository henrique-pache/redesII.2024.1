import pyaudio
import socket
import time

# Configurações de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096  # Aumentando o tamanho do chunk

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
        start_time = time.time()  # Marca o tempo de início do processamento do chunk
        data, addr = sock.recvfrom(65536)  # Recebe os dados do chunk
        stream.write(data)  # Escreve no stream de áudio
        end_time = time.time()  # Marca o tempo de fim do processamento do chunk
        
        # Calcula o tempo necessário para processar o chunk
        processing_time = end_time - start_time
        print(f"o tempo de processamento foi de: {processing_time}")
        # Calcula o tempo de espera para o próximo chunk
        # Subtrai o tempo de processamento do chunk do tempo de espera desejado
        wait_time = max(0, CHUNK / RATE - processing_time)
        
        # Aguarda dinamicamente antes de receber o próximo chunk
        time.sleep(wait_time)
except KeyboardInterrupt:
    print("Recepção finalizada.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
