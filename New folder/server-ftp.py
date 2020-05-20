import socket
import random
import select
import sys
import os
import zipfile

server_address = ('127.0.0.1',5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)

list_of_clients=[]

def broadcast(address, addr, message):
    #print("YAY! YOU CALLED ME!!!!!!")
    for clients in list_of_clients:
        if clients!=address: 
            server_socket.sendto(addr.encode(), clients)
            server_socket.sendto(message.encode(), clients)

def broadcastfile(address, filename):
    #print("YAY! YOU CALLED ME!!!!!!")
    for clients in list_of_clients:
        if clients!=address: 
            message='itsafile'
            server_socket.sendto(message.encode(),clients)
            server_socket.sendto(filename.encode(),clients)
            filesize = os.path.getsize(filename)
            filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
            server_socket.sendto(filesize.encode(),clients)
            file_to_send = open(filename, 'rb')
            l = file_to_send.read()
            server_socket.sendto(l,clients)
            file_to_send.close()
            print('Broadcasted to'+'<\'' +str(clients[0])+'\',\''+str(clients[1])+'\'>')

while True:
    data, client_address = server_socket.recvfrom(1024)
    list_of_clients.append(client_address)
    list_of_clients = list(set(list_of_clients))
    message = data.decode()
    if(message=='itsafile'):
        address = client_address
        data, client_address = server_socket.recvfrom(1024)
        filename = data.decode()
        data, client_address = server_socket.recvfrom(1024)
        filesize = data.decode()
        filesize = int(filesize, 2)
        file_to_write = open(filename, 'wb')
        chunksize = 4096
        while filesize > 0:
            if filesize < chunksize:
                chunksize = filesize
            data, client_address = server_socket.recvfrom(1024)
            data = data
            file_to_write.write(data)
            filesize -= len(data)
        file_to_write.close()
        print('Received File : '+filename + " Broadcasting... ")
        broadcastfile(address,filename)
    else:
        addr='<\'' +str(client_address[0])+'\',\''+str(client_address[1])+'\'>'
        print('\n>> '+ addr+' '+message)
        broadcast(client_address,addr, message)

list_of_clients.remove(data)
data.close()