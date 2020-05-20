import socket
import sys
from threading import Thread

# konfigurasi server connect
server_address = ('localhost', 3000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting to %s port %s' % server_address)
client.connect(server_address)

# gui
from tkinter import *
# main window
mw = Tk()
mw.option_add("*Button.Background", "grey")
mw.option_add("*Button.Foreground", "white")
mw.title('ChatApp')
mw.geometry("500x500") #ukuran 500x500
mw.resizable(0, 0) #Don't allow resizing in the x or y direction

# back frame
back = Frame(master=mw,bg='grey')
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=BOTH, expand=1) #Expand the frame to fill the root window

# list box & scrollbar
Lb = Listbox(back)
Lb.pack(side = LEFT, fill=BOTH, expand=1)
scrollbar = Scrollbar(back)
scrollbar.pack(side = RIGHT, fill = BOTH)
Lb.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = Lb.yview)

# get inputan
def getTextInput():
    message = textExample.get("1.0","end-1c")
    print(message)
    client.send(message.encode())

# input box
textExample=Text(master=mw, height=1)
textExample.pack()
btnRead=Button(master=mw, height=1, width=10, text="Send ", command=getTextInput)
btnRead.pack()

# get broadcast
def recv():
    while True:
        data = client.recv(1024).decode()
        print(data)
        ###
        Lb.insert(END, data)
        textExample.delete('1.0', END)

Thread(target=recv).start()
mw.mainloop()