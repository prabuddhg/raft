from curio import run, tcp_server, Lock, TaskGroup, Queue, sleep
import messages as msg

lock = Lock()
messages = Queue()
subscribers = set()


async def dispatcher():
    while True:
        msg = await messages.get()
        for q in subscribers:
            await q.put(msg)


# Publisher
async def publish(msg):
    await messages.put(msg)


# Task that writes chat messages to clients
async def outgoing(client_stream):
    queue = Queue()
    try:
        subscribers.add(queue)
        while True:
            name, msg = await queue.get()
            await client_stream.write(name + b":" + msg)
    finally:
        subscribers.discard(queue)


# task that reads chat messages and publishes them
async def incoming(client_stream, name):
    async for line in client_stream:
        await publish(name, line)


async def chat_handler(client, addr):
    print(f"Connection from {addr}")
    async with client.as_stream() as s:
        async for line in s:
            decoded_line = line.decode("utf-8").strip()
            print(f"received from {addr}: {decoded_line}")
            async with lock:
                ret_msg = msg.process(decoded_line)
                await s.write(ret_msg.encode("utf-8"))
    print("Connection closed")


if __name__ == "__main__":
    msg.recover()
    run(tcp_server, "", 25000, echo_client)
