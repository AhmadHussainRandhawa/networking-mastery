import socket
import select


class TinyEventLoop():
    
    def __init__(self):
        self._read_callbacks = {}
        self._write_callbacks = {}

    def register_read(self, sock, callback):
        self._read_callbacks[sock] = callback

    def register_write(self, sock, callback):
        self._write_callbacks[sock] = callback

    def unregister(self, sock):
        self._read_callbacks.pop(sock, None)
        self._write_callbacks.pop(sock, None)


    def run(self):
        while True:

            if not self._read_callbacks and not self._write_callbacks:
                break

            read_sockets = list(self._read_callbacks.keys())
            write_sockets = list(self._write_callbacks.keys())

            readable, writable, _ = select.select(read_sockets, write_sockets, [])

            for sock in readable:
                callback = self._read_callbacks.get(sock)
                if callback:
                    callback(sock)

            for sock in writable:
                callback = self._write_callbacks.get(sock)
                if callback:
                    callback(sock)


'''
def main():
    event_loop = TinyEventLoop()

    reader, writer = socket.socketpair()

    counter = {"count": 0}

    def read_callback(sock):
        data = sock.recv(1024)
        print("Received:", data.decode())
        counter["count"] += 1

        if counter["count"] == 3:
            event_loop.unregister(sock)
            sock.close()
            writer.close()

    event_loop.register_read(reader, read_callback)

    writer.send(b"Message 1")
    writer.send(b"Message 2")
    writer.send(b"Message 3")

    event_loop.run()

if __name__ == '__main__':
    main()
'''