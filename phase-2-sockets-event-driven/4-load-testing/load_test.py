import socket
import threading
import time


HOST = "127.0.0.1"
PORT = 5000

NUM_CLIENTS = 100
MESSAGES_PER_CLIENT = 100


def client_worker():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        message = b"hello world"

        for _ in range(MESSAGES_PER_CLIENT):
            sock.sendall(message)

        sock.close()

    except Exception as e:
        print("Client error:", e)


def main():
    threads = []

    start_time = time.perf_counter()

    for _ in range(NUM_CLIENTS):
        t = threading.Thread(target=client_worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.perf_counter()

    total_messages = NUM_CLIENTS * MESSAGES_PER_CLIENT
    total_time = end_time - start_time

    print("Total messages:", total_messages)
    print("Total time:", total_time)
    print("Messages per second:", total_messages / total_time)


if __name__ == "__main__":
    main()