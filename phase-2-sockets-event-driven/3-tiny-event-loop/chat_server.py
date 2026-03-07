import socket
from tiny_event_loop import TinyEventLoop


HOST = "0.0.0.0"
PORT = 5000

event_loop = TinyEventLoop()
clients = {}


def create_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)
    return server


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")

    client_socket.setblocking(False)

    state = {
        "addr": client_address,
        "socket": client_socket,
        "out_buffer": bytearray(),
    }

    clients[client_socket] = state

    event_loop.register_read(client_socket, handle_read)


def broadcast(message, sender_socket):
    for sock, state in clients.items():

        if sock is sender_socket:
            continue

        state["out_buffer"] += message
        event_loop.register_write(sock, handle_write)


def handle_read(sock):
    state = clients[sock]

    try:
        data = sock.recv(4096)

        if not data:
            disconnect(sock)
            return

        print(f"Received: {data.decode()}")
        broadcast(data, sock)

    except (ConnectionResetError, OSError):
        disconnect(sock)


def handle_write(sock):
    state = clients[sock]

    try:
        if state["out_buffer"]:
            sent = sock.send(state["out_buffer"])
            state["out_buffer"] = state["out_buffer"][sent:]

        if not state["out_buffer"]:
            event_loop._write_callbacks.pop(sock, None)

    except OSError:
        disconnect(sock)


def disconnect(sock):
    state = clients.get(sock)

    if state:
        print(f"Client {state['addr']} disconnected")

    event_loop.unregister(sock)
    clients.pop(sock, None)
    sock.close()


def main():
    server_socket = create_server_socket()

    event_loop.register_read(server_socket, accept_connection)

    print(f"Chat server running on {HOST}:{PORT}")

    event_loop.run()


if __name__ == "__main__":
    main()