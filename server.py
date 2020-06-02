import socket
from threading import Thread

def accept_conn():
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=run_client, args=(client,)).start()

def run_client(client): 
    user = client.recv(buffer).decode()
    welcome = 'Welcome %s! ' % user
    client.send(welcome.encode() )
    msg = "%s has joined the chat!" % user
    broadcast(msg.encode() )
    clients[client] = user
 
    while True:
        msg = client.recv(buffer)
        broadcast(msg, user + " : ")

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(prefix.encode() +msg)

clients = {}
addresses = {}

host = 'localhost'
port = 3000

buffer = 1024
addr = (host, port)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(addr)

if __name__ == "__main__":
    server.listen(5)
    print("Waiting connection...")
    acc_thread = Thread(target=accept_conn)
    acc_thread.start()
    acc_thread.join()
    server.close()