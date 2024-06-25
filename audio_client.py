import socket
import sys
import json
import pyaudio

def main():
    if len(sys.argv) != 5:
        print("Usage: python audio_client.py -t <TOPIC> -m <IP:PORT>")
        sys.exit(1)
    
    topic = sys.argv[2]
    ip, port = sys.argv[4].split(":")
    client_address = (ip, int(port))
    
    # Conectar ao broker
    broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_socket.connect(("localhost", 8888))
    
    # Publicar mensagem
    message = json.dumps({"type": "publish", "topic": topic, "data": f"{ip}:{port}"})
    broker_socket.sendall(message.encode("utf-8"))
    print(f"Published message to topic {topic} with address {ip}:{port}")
    
    # Preparar para receber dados via UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(client_address)
    
    # Configurar PyAudio para reprodução
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True,
                        frames_per_buffer=512)
    
    while True:
        data, addr = udp_socket.recvfrom(512)
        print(f"Received from {addr}: {len(data)} bytes")
        stream.write(data)

if __name__ == "__main__":
    main()
