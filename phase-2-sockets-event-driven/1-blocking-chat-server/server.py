import socket

HOST = "0.0.0.0"
PORT = 5000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

if __name__ == "__main__":
    main()