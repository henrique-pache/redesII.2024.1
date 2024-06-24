import socket
from pydub import AudioSegment
import time

# Configurações do arquivo de áudio
FILENAME = 'rock.mp3'  # Substitua pelo caminho do seu arquivo de áudio MP3

# Configurações do socket UDP
UDP_IP = "127.0.0.1"  # Endereço IP do receptor
UDP_PORT = 5005       # Porta do receptor

# Inicializa o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Transmissão iniciada...")

try:
    # Abre o arquivo de áudio e converte para PCM
    audio = AudioSegment.from_mp3(FILENAME)
    
    # Verifica e ajusta a taxa de amostragem para 44100 Hz e o número de canais para mono
    audio = audio.set_frame_rate(44100).set_channels(1)
    
    # Obtém os dados de áudio brutos
    raw_audio = audio.raw_data
    
    print(f"Tamanho total dos dados de áudio: {len(raw_audio)} bytes")
    
    # Calcula o tempo total de reprodução em segundos
    duration_sec = len(audio) / 1000.0  # em milissegundos
    
    # Calcula o número de chunks e o tempo de reprodução de cada chunk
    num_chunks = int(duration_sec * 10)  # dividindo em 10 partes aproximadamente
    chunk_duration = duration_sec / num_chunks
    
    print(f"Número de chunks: {num_chunks}")
    print(f"Duração de cada chunk: {chunk_duration} segundos")
    
    # Envia os dados de áudio em chunks de acordo com o tempo de reprodução de cada um
    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = (i + 1) * chunk_duration
        
        # Obtém o chunk de áudio para o intervalo de tempo atual
        chunk = audio[int(start_time * 1000):int(end_time * 1000)]
        chunk_data = chunk.raw_data
        
        # Envia o chunk
        sock.sendto(chunk_data, (UDP_IP, UDP_PORT))
        print(f"Enviando chunk {i + 1}/{num_chunks} - Tamanho: {len(chunk_data)} bytes")
        
        # Aguarda o tempo restante até o próximo chunk
        #95% do tempo para evitar que o receptor reproduza mais rapido do que o transmissor
        time.sleep(chunk_duration*0.95)
    
    print("Transmissão finalizada.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    sock.close()
