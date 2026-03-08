import asyncio
import time

HOST = "127.0.0.1"
PORT = 5000

NUM_CLIENTS = 10000
MESSAGES_PER_CLIENT = 20

MESSAGE = b"hello\n"


async def client_worker():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)

        for _ in range(MESSAGES_PER_CLIENT):
            writer.write(MESSAGE)
            await writer.drain()

        writer.close()
        await writer.wait_closed()

    except Exception:
        pass


async def run_test():
    tasks = []

    start = time.time()

    for _ in range(NUM_CLIENTS):
        tasks.append(asyncio.create_task(client_worker()))

    await asyncio.gather(*tasks)

    end = time.time()

    total_messages = NUM_CLIENTS * MESSAGES_PER_CLIENT
    total_time = end - start

    print("Clients:", NUM_CLIENTS)
    print("Total messages:", total_messages)
    print("Total time:", total_time)
    print("Messages/sec:", total_messages / total_time)


if __name__ == "__main__":
    asyncio.run(run_test())