import socket
import sys
# import threading
from threading import Thread

server_address = ('localhost', 3000)

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
print('connecting to %s port %s' % server_address)
client.connect(server_address)

def recv():
    # Read responses on both sockets
    while True:
        data = client.recv(1024).decode()
        print(data)
            # if not data:
            #     print('closing socket', s.getsockname() )
            #     s.close()


Thread(target=recv).start()

while True:
    message = sys.stdin.readline() 
    print('sending %s' %message )
    client.send(message.encode())

