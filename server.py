import re as r
import socket
import threading
from urllib.request import urlopen

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddr = s.getsockname()[0]
s.close()


PORT = 7346
ADDR = (ipaddr, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connected_conn = []

def broadcast_msg(msg):
    for conn in connected_conn:
        conn.send(msg.encode(FORMAT))


def handle_client(conn, addr):
    connected_conn.append(conn)
    print(f'NEW CONNECTION {addr}')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            print(f'{addr}---->{msg}')
            # broadcast_msg(msg)
            if msg == DISCONNECT:
                connected = False
            conn.send("Message Recieved".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f'SERVER IS LISTENNINg.......')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args=(conn, addr))
        thread.start()
        print(f'ACTIVE CONNECTION = {threading.active_count() - 1}')

print(f"SERVER CONFIG: {ADDR}")
start()
