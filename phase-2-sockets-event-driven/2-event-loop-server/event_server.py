import socket
import selectors

HOST = '0.0.0.0'
PORT = 5000

selector = selectors.DefaultSelector()


def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)
    return server_socket


def accept_connection(server_socket):
    client_socket, client_addr = server_socket.accept()
    print(f"New connection from {client_addr}")

    client_socket.setblocking(False)
    selector.register(client_socket, selectors.EVENT_READ, data="client")


def event_loop():
    while True:
        events = selector.select()

        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                client_socket = key.fileobj
                data = client_socket.recv(1024)

                if not data:
                    print('Client Disconnected')
                    selector.unregister(client_socket)
                    client_socket.close()
                else:
                    print(f"The received data: {data.decode()}")


def main():
    server_socket = create_server_socket()

    selector.register(server_socket, selectors.EVENT_READ, data=None)

    print(f'Event-driven server running on {HOST}:{PORT}')
    event_loop()


if __name__ == '__main__':
    main()