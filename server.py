import sys
import socket
import types
import selectors
from typing import Optional

from commSupport import *

# Globals
sel = selectors.DefaultSelector()

# Command line arguments for host and ports

# host = sys.argv[1]
cmd_port = int(sys.argv[1]) # Only works for ints currently
                            # Accept empty string and error when non-digit 

# Storage of user and their ip and port
addr_rec = {}
client_name = ""
# Change to dictionary. Key being username and value being the ip port tuple

# Functions
def accept_wrapper(sock: socket.socket):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")

    active_conns = "Currently active connections:"
    for i in addr_rec: # Send username and ip, port of user
        active_conns += (f"\nUser {i}: IP = {addr_rec[i][0]}, Port = {addr_rec[i][1]}")
    conn.send(active_conns.encode()) # Use conn.send not sock.send 

    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # Accept read and writing for client
    sel.register(conn, events, data=data)

def service_connection(key: selectors.SelectorKey, mask):
    sock = key.fileobj # Key holds socket information
    # .fileobj is the socket representation
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            if USERNAME_PREFIX in recv_data.decode():
                username = recv_data[USERNAME_LEN::].decode()
                addr_rec[username] = data.addr
                # addr is tuple in form (ip addr, client port num)
                return
            data.outb += recv_data
        else:
            print(f"EOF received, closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb.decode()} to {data.addr}") # Decode to print as string
            sent = sock.send("Server has sent: ".encode() + data.outb) # Send received data back to client without changes
            data.outb = data.outb[sent:] # Index list to make blank

def print_all_keys(key: selectors.SelectorKey):
    
    for i in range(4):
        print(key[i])

# Setup function (split it up into smaller chunks later)
class ServerSetup:
    def __init__(self, host: Optional[str], port: Optional[int]) -> types.NoneType:
        if host == None:
            # Get private ip address through currently connected WiFi
            self._host = socket.gethostbyname(socket.gethostname())
        else:
            self._host = host
        
        if port == None: # No port specified, set as ephemeral port
            self._port = 0
        else:
            self._port = port

    def get_host(self) -> str:
        return self._host

    def get_port(self) -> int:
        return self._port

    def init_server(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        host = self.get_host()
        port = self.get_port()
        print(f"hostname is {hostname}, ip addr is {host}") 

        sock.bind((host, port))
        sock.listen()
        print(f"Listening on {(host, sock.getsockname()[1])}")
        sock.setblocking(False) # Prevent blocking of system calls, i.e. allows 
                                # sockets to handle multiple client requests

        sel.register(sock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=1) # Timouts for 1 second waiting for new
                                            # connections. Allows 1 second before 
                                            # terminating server if ^C received
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
        except KeyboardInterrupt:
            print("Keyboard Interrupt, aborting...")
            print(f"Total connections: {len(addr_rec)}\nActive connections: {addr_rec}")
        finally:
            sel.close()

server = ServerSetup(None, cmd_port)
server.init_server()