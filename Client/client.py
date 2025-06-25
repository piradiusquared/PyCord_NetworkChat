import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Hi this is the client", b"Hi, another message from client!"]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)

def create_connection(host, port):
    server_addr = (host, port)

    try:
        print(f"Starting connection 1 to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr) # Connect to specified host and port
                                  # Currently testing on localhost only
        while True:
            a = input("Type a message to send: ")
            sock.send(a.encode())
            print(sock.recv(1024).decode())
        # sock.send("Hello from client".encode())

    except KeyboardInterrupt:
        print("Interrupted, aborting...")

# Soon, wrap this around with error checking and print error messages
# host = sys.argv[1] 
port = int(sys.argv[1]) # Currently testing on localhost only
# num_conns = int(sys.argv[3])
create_connection("127.0.0.1", port)