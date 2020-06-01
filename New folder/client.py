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
from threading import Thread

def login():
	# print(e1.get(), e2.get())
	name = e1.get()
	client.send(name.encode())
	top.destroy()

def getTextInput():
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

def recv():
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
						eula.config(state=NORMAL)
						eula.insert(END, data + "\n")
						eula.config(state=DISABLED)
						e3.delete(0, 'end')

if __name__ == '__main__':
	#server configuration
	server_address = ('localhost', 5000)
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.connect(server_address)

	mw = Tk()
	mw.option_add("*Button.Background", "grey")
	mw.option_add("*Button.Foreground", "white")
	mw.title('ChatApp')
	mw.geometry("500x400") #ukuran 500x500
	mw.resizable(0, 0) #Don't allow resizing in the x or y direction
	# back frame
	back = Frame(master=mw,bg='grey')
	back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
	back.pack(fill=BOTH,expand=1) #Expand the frame to fill the root window
	# Vertical (y) Scroll Bar
	scroll = Scrollbar(back)
	scroll.pack(side=RIGHT, fill=Y)

	# Text Widget
	eula = Text(back, wrap=NONE, yscrollcommand=scroll.set)
	# eula.insert(END, "\ntext")
	eula.pack(side="left")
	eula.config(state=DISABLED)
	# Configure the scrollbars
	scroll.config(command=eula.yview)

	Thread(target=recv).start()

	# input box
	# btnFtp=Button(master=mw, height=1, text=" $ ", command=getFileInput)
	# btnFtp.pack(side=LEFT)
	e3 = Entry(mw, width=72)
	e3.pack(side=LEFT)
	# textExample=Text(master=mw, height=1)
	# textExample.pack()
	btnRead=Button(master=mw, height=1, text=" Send ", command=getTextInput)
	btnRead.pack(side=LEFT)

	top = Toplevel()
	topbg = Frame(master=top,bg='grey', height=50)
	topbg.pack(fill=X, expand=1) #Expand the frame to fill the root window
	Label(topbg, text="Username : ").pack(pady = 4)
	e1 = Entry(topbg, width=25)
	e1.pack(pady = 4)
	Label(topbg, text="Password : ").pack(pady = 4)
	e2 = Entry(topbg, show="*", width=25)
	e2.pack(pady = 4)
	Button(topbg, text='Login', command=login).pack()

	mw.mainloop()