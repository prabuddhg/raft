import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10000  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "Hello, World"
    s.sendall(message.encode("utf-8"))
    data = s.recv(1024)
    print(f"Received {data}")
