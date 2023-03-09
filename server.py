from curio import run, tcp_server, Lock, TaskGroup, Queue, sleep
import messages as msg
import argparse
import constants as const
import socket
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
log = logging.getLogger()

lock = Lock()
messages = Queue()
subscribers = set()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--server", dest="server", help="1 for server1, 2 for server 2"
    )
    # Parse and print the results
    args = parser.parse_args()
    return args


class RaftNode:
    def __init__(self, port_number, ip_address="127.0.0.1", peers=None):
        self.port_number = port_number
        self.ip_address = ip_address
        self.peers = peers

    async def dispatcher(self):
        while True:
            msg = await messages.get()
            for q in subscribers:
                await q.put(msg)

    # Publisher
    async def publish(self, msg):
        await messages.put(msg)

    # Task that writes chat messages to clients
    async def outgoing(self, client_stream):
        queue = Queue()
        try:
            subscribers.add(queue)
            while True:
                name, msg = await queue.get()
                output = name + b":" + msg.encode("utf-8")
                await client_stream.write(output)
        finally:
            subscribers.discard(queue)

    # task that reads chat messages and publishes them
    async def incoming(self, client_stream, name):
        async for line in client_stream:
            decoded_line = line.decode("utf-8").strip()
            ret_msg = msg.process(decoded_line)
            await self.publish((name, ret_msg))

    async def chat_handler(self, client, addr):
        print("Connection from", addr)
        async with client:
            client_stream = client.as_stream()
            await client_stream.write(b"Your name: ")
            name = (await client_stream.readline()).strip()
            # await publish((name, b'joined\n'))
            while True:
                async with TaskGroup(wait=any) as workers:
                    await workers.spawn(self.outgoing, client_stream)
                    await workers.spawn(self.incoming, client_stream, name)

            await publish((name, b"has gone away\n"))

        log.info("Connection closed")

    async def chat_server(
        self,
    ):
        msg.recover()
        async with TaskGroup() as g:
            await g.spawn(self.dispatcher)
            await g.spawn(
                tcp_server, self.ip_address, self.port_number, self.chat_handler
            )


if __name__ == "__main__":
    args = get_args()
    port_number, peers = const.get_port_number(args.server)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    log.info(f"Starting raft node#{args.server} for ip:{ip_address} and {port_number} with peers: {peers}")
    raft_node = RaftNode(port_number, ip_address, peers)
    run(raft_node.chat_server())
