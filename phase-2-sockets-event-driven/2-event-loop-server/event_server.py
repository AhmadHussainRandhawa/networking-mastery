import socket
import selectors

HOST = "0.0.0.0"
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
    try:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        client_socket.setblocking(False)

        state = {
            "addr": client_address,
            "out_buffer": bytearray(),
            "socket": client_socket,
        }

        selector.register(client_socket, selectors.EVENT_READ, data=state)

    except OSError as e:
        print("Accept error:", e)


def broadcast(message, sender_socket):
    for key in selector.get_map().values():
        state = key.data

        if state is None:
            continue  # skip server socket

        client_socket = state["socket"]

        if client_socket is sender_socket:
            continue

        state["out_buffer"] += message

        # Ensure socket is registered for write events
        selector.modify(client_socket, selectors.EVENT_READ | selectors.EVENT_WRITE, data=state)


def handle_read(key):
    state = key.data
    client_socket = state["socket"]

    try:
        data = client_socket.recv(4096)

        if not data:
            disconnect(client_socket)
            return

        print(f"Received: {data.decode()}")
        broadcast(data, client_socket)

    except (ConnectionResetError, OSError):
        disconnect(client_socket)


def handle_write(key):
    state = key.data
    client_socket = state["socket"]

    try:
        if state["out_buffer"]:
            sent = client_socket.send(state["out_buffer"])
            state["out_buffer"] = state["out_buffer"][sent:]

        # If nothing left to send, stop monitoring write
        if not state["out_buffer"]:
            selector.modify(client_socket, selectors.EVENT_READ, data=state)

    except (BlockingIOError):
        return
    except (ConnectionResetError, BrokenPipeError, OSError):
        disconnect(client_socket)


def disconnect(client_socket):
    try:
        state = selector.get_key(client_socket).data
        print(f"Client {state['addr']} disconnected")
        selector.unregister(client_socket)
        client_socket.close()
    except Exception:
        pass


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