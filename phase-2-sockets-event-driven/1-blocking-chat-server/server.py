import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
lock = threading.Lock()


def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.sendall(message)
                except Exception:
                    pass


def handle_client(client_socket, client_addr):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data: 
                print(f"Client {client_addr} disconnected")
                break
            
            print(f"Received from {client_addr}: {data.decode()}")

            # Broadcast to others
            broadcast(data, client_socket)

        except Exception:
            break

    # Remove client safely
    with lock: 
        if client_socket in clients:
            clients.remove(client_socket)    

    client_socket.close()
    print(f"Client {client_addr} disconnected")



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        with lock:
            clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()