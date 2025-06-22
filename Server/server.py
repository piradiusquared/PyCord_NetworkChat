import sys
import socket
import types
import selectors

# Globals
sel = selectors.DefaultSelector()

# Command line arguments for host and ports

# host = int(sys.argv[1])
# port = int(sys.argv[2])

host = "127.0.0.1"
port = 12345

# Functions
def accept_wrapper(sock: socket.socket):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # Accept read and writing for client
    sel.register(conn, events, data=data)

def service_connection(key: selectors.SelectorKey, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"EOF received, closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False) # Prevent blocking of system calls. i.e. Allow system 
#to catch immediate ^C calls and terminate server

sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None) # Blocks until sockets are available
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Keyboard Interrupt, aborting...")
finally:
    sel.close()