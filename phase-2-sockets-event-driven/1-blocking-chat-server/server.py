import socket
import threading

HOST = "0.0.0.0"
PORT = 5000


def handle_client(conn, client_addr):
    while True:
        try:
            data = conn.recv(1024)
            
            if not data: 
                print(f'Client {client_addr}: disconnected')
                break

            print(f"Received from {client_addr}: {data.decode()}")

        except ConnectionResetError:
            print(f'Client {client_addr}: Disconnected')
            break
    
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        thread = threading.Thread(
            target=handle_client,
            args=(conn, client_address),
            daemon=True
        )
        thread.start()

if __name__ == "__main__":
    main()