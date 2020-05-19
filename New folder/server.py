import socket
from threading import Thread

def accept_conn():
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send("Type your name...".encode() )
        addresses[client] = client_address
        Thread(target=run_client, args=(client,)).start()

def run_client(client):  # Takes client socket as argument.
    user = client.recv(buffer).decode()
    welcome = 'Welcome %s! type quit to exit program.' % user
    client.send(welcome.encode() )
    msg = "%s has joined the chat!" % user
    broadcast(msg.encode() )
    clients[client] = user

    while True:
        msg = client.recv(buffer)
        # if msg != "quit".encode():
        broadcast(msg, user + " : ")
        # else:
        #     client.send("quit".encode() )
        #     client.close()
        #     del clients[client]
        #     broadcast(user.encode() + " has left the chat.".encode())
        #     break

def broadcast(msg, prefix=""):  # prefix is for name identification.
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