import socket
import pyaudio
import threading

# Настройки аудио
FORMAT = pyaudio.paInt16  # Формат звука
CHANNELS = 1               # Количество каналов (1 для моно)
RATE = 44100               # Частота дискретизации
CHUNK = 1024               # Размер блока данных

def handle_client(conn):
    print("Клиент подключен.")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data = conn.recv(CHUNK)
            if not data:
                break
            stream.write(data)  # Проигрывание аудио
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        conn.close()
        print("Клиент отключен.")

def start_server():
    host = '0.0.0.0'  # Будем слушать на всех интерфейсах
    port = 5000       # Порт для прослушивания

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}. Ожидание подключения...")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()