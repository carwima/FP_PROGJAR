import socket
import select
import sys
import msvcrt
import os
from ftplib import FTP
import os
import shutil
from zipfile import ZipFile
from tkinter import *
from tkinter import filedialog

f_user = 'test'
f_password = ''
ip_ftp = '127.0.0.1'
f = FTP(ip_ftp)
f.login(f_user,f_password)
server_address = ('localhost', 5000)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.connect(server_address)
delay = 1
starter = ' Connected!'
print('You are connected!')
server.send(starter.encode())

while True:
    socket_list = [server]
    read_socket, write_socket, error_socket = select.select(socket_list,[],[],1)
    if msvcrt.kbhit(): 
        read_socket.append(sys.stdin)
    for socks in read_socket:
        if socks==server:#baca
            message = server.recv(2048).decode()
            if message:
                if(message=='itsafile'):
                    filename = server.recv(2048).decode()
                    filesize = server.recv(2048).decode()
                    filesize = int(filesize, 2)
                    file_to_write = open(filename, 'wb')
                    chunksize = 4096
                    while filesize > 0:
                        if filesize < chunksize:
                            chunksize = filesize
                        data = server.recv(2048)
                        file_to_write.write(data)
                        filesize -= len(data)
                    file_to_write.close()
                    print('Received File : '+filename)
                else:
                    sender = message
                    message = server.recv(2048).decode()
                    print(sender +' '+ message)
            print('Current working directory ' + f.pwd()+ '\n')
        else: #kirim
            message = sys.stdin.readline()
            if(message.split(' ')[0]=='SENDALL'): #stringcheck
                filename=str(str(message.split(' ')[1]).split('\n')[0])
                message='itsafile'
                server.send(message.encode())
                server.send(filename.encode())
                filesize = os.path.getsize(filename)
                filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
                server.send(filesize.encode())
                file_to_send = open(filename, 'rb')
                l = file_to_send.read()
                server.sendall(l)
                file_to_send.close()
            else:
                message=message.split('\n')
                server.send(message[0].encode())
                server.settimeout(delay)
            print('Current working directory ' + f.pwd() + '\n')
server.close() 