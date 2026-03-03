import socket
import time

HOST = '127.0.0.1'  # localhost
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    for i in range(5000):
        message = "X"         # "X" * 1000: 1 KB per message
        start = time.perf_counter()
        s.sendall(message.encode())
        data = s.recv(1024)
        end = time.perf_counter()
        print(f"Sent: {message} | Received: {data.decode()} | RTT: {end-start:.6f}s")
