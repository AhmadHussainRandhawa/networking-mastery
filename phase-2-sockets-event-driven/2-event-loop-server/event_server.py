import socket
import selectors

HOST = "0.0.0.0"
PORT = 5000

selector = selectors.DefaultSelector()
connections = {}


def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)
    return server_socket


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")

    client_socket.setblocking(False)

    connections[client_socket] = {
        "addr": client_address,
        "out_buffer": b"",
    }

    selector.register(client_socket, selectors.EVENT_READ)


def broadcast(message, sender_socket):
    for client_socket, state in connections.items():
        if client_socket != sender_socket:
            state["out_buffer"] += message

            # Ensure socket is registered for write events
            selector.modify(
                client_socket,
                selectors.EVENT_READ | selectors.EVENT_WRITE
            )


def handle_read(key):
    client_socket = key.fileobj
    try:
        data = client_socket.recv(1024)
    except ConnectionResetError:
        data = None
        
    if not data:
        disconnect(client_socket)
        return

    print(f"Received: {data.decode()}")
    broadcast(data, client_socket)


def handle_write(key):
    client_socket = key.fileobj
    state = connections[client_socket]

    if state["out_buffer"]:
        try:
            sent = client_socket.send(state["out_buffer"])
            state["out_buffer"] = state["out_buffer"][sent:]
        except BlockingIOError:
            return

    # If nothing left to send, stop monitoring write
    if not state["out_buffer"]:
        selector.modify(client_socket, selectors.EVENT_READ)


def disconnect(client_socket):
    print(f"Client {connections[client_socket]['addr']} disconnected")
    selector.unregister(client_socket)
    client_socket.close()
    del connections[client_socket]


def event_loop():
    while True:
        events = selector.select()

        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                if mask & selectors.EVENT_READ:
                    handle_read(key)

                if mask & selectors.EVENT_WRITE:
                    handle_write(key)


def main():
    server_socket = create_server_socket()
    selector.register(server_socket, selectors.EVENT_READ, data=None)

    print(f"Event-driven chat server running on {HOST}:{PORT}")
    event_loop()


if __name__ == "__main__":
    main()