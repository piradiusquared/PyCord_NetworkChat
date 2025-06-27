import sys
import socket
import selectors
import types

from clientSupport import *

class TestCases:
    def __init__(self, host, port, num_conns) -> types.NoneType:
        self._host = host
        self._port = port
        self._num_conns = num_conns

    def test_multiple_connections(host, port, num_conns) -> None:
        sel = selectors.DefaultSelector()
        messages = [b"Hi this is the client", b"Hi, another message from client!"]
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
        print(f"Initialising connection to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock == -1:
            print("Could not establish socket") # Should rarely/never happen
            return
        
        # Attempt to connect to server
        try:
            sock.connect(server_addr) # Connect to specified host and port
                                  # Currently testing on localhost only
        except ConnectionRefusedError:
            print(PORT_ERROR)
            exit(PORT_EXIT)

        
        while True:
            a = input("Type a message to send: ")
            if len(a) == 0: # Filter out empty messages which hang the client
                print("Cannot send empty messages!")
            else:
                sock.send(a.encode())
                receive = sock.recv(1024).decode() # Currently only support receiving 1024 bytes
                                               # Future addition: allow larger transmission of reasonable size
                print(receive)
            

    except KeyboardInterrupt:
        print("Interrupted, aborting...")
        sys.exit(1) # Exit client

def main():
    # host = sys.argv[1] # Only using localhost for current version

    if len(sys.argv) < 2:
        print(USAGE_ERROR)
        exit(USAGE_EXIT) # Exit code 8

    port = int(sys.argv[1]) # Get port specified by user
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    print(f"hostname is {hostname}, ip addr is {ip_addr}") 
    create_connection(ip_addr, port)    
    
    return 0

if __name__ == "__main__":
    main()
