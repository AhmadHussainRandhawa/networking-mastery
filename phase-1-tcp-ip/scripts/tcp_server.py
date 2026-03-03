import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)

def handle_client(conn, addr):
    with conn:
        print("Connected:", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

if __name__ == "__main__":
    main()



# conn  # a NEW socket object (dedicated to that client)
# addr  # (ip, port) of the client