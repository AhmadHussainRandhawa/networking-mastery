import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

NUM_CLIENTS = 100
MESSAGES_PER_CLIENT = 500

def client_task(client_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        for i in range(MESSAGES_PER_CLIENT):
            message = f"Client {client_id} message {i}"
            s.send(message.encode())
            time.sleep(0.01)

        s.close()

    except Exception as e:
        print(f"Client {client_id} error: {e}")

threads = []

start_time = time.time()

for i in range(NUM_CLIENTS):
    t = threading.Thread(target=client_task, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end_time = time.time()

print("Load test completed")
print("Total time:", end_time - start_time)