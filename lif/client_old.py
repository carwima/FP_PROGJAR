import socket
import sys
from threading import Thread
from tkinter import *
from tkinter import filedialog
from ftplib import FTP

f_user = 'lif_FP'
f_password = ''
ip_ftp = '127.0.0.1'
f = FTP(ip_ftp)
f.login(f_user,f_password)
session = FTP(ip_ftp, f_user, f_password)

name =""

# get inputan
def getTextInput():
    message = e3.get()
    if message[0:5]=='/retr':
        filename = message[6:]
        localfile = open(filename, 'wb')
        session.retrbinary("RETR " + filename, localfile.write, 1024)
        localfile.close()
        
    # print(message)
    else:
        client.send(message.encode())

def getFileInput():
    filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =( ("jpeg files","*.jpg"),("all files","*.*") ) )
    client.send(filename.encode())
    file = open(filename,'rb')    
    filename=filename.split("/")[-1]              # file to send
    session.storbinary('STOR '+filename, file)     # send the file
    file.close()
    pesanfilekirim = name+" telah mengirim file dengan nama "+filename+". Silakan kirim pesan /retr "+filename+" untuk mengunduh file."
    client.send(pesanfilekirim.encode())


# get broadcast
def recv():
    while True:
        data = client.recv(1024).decode()
        eula.config(state=NORMAL)
        eula.insert(END, data + "\n")
        eula.config(state=DISABLED)
        e3.delete(0, 'end')
        # Lb.insert(END, data)
        # textExample.delete('1.0', END)

def login():
    # print(e1.get(), e2.get())
    name = e1.get()
    client.send(name.encode())
    top.destroy()
 


if __name__ == '__main__':
    # konfigurasi server connect
    server_address = ('localhost', 3000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting to %s port %s' % server_address)
    client.connect(server_address)
    

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
    eula = Text(back, wrap=WORD, yscrollcommand=scroll.set)
    # eula.insert(END, "\ntext")
    eula.pack(side="left")
    eula.config(state=DISABLED)
    # Configure the scrollbars
    scroll.config(command=eula.yview)

    Thread(target=recv).start()

    # input box
    btnFtp=Button(master=mw, height=1, text=" $ ", command=getFileInput)
    btnFtp.pack(side=LEFT)
    e3 = Entry(mw, width=72)
    e3.pack(side=LEFT)
    # textExample=Text(master=mw, height=1)
    # textExample.pack()
    photo = PhotoImage(file = "gui assets/send.png") 
    photoimage = photo.subsample(7, 7)
    btnRead=Button(master=mw, height=1, text=" Send ", image = photoimage, compound = LEFT, command=getTextInput)
    btnRead.pack(side=LEFT)
    

    top = Toplevel()
    topbg = Frame(master=top,bg='grey', height=50)
    topbg.pack(fill=X, expand=1) #Expand the frame to fill the root window
    Label(topbg, text="Username : ").pack(pady = 4)
    e1 = Entry(topbg, width=25)
    e1.pack(pady = 4)
    # Label(topbg, text="Password : ").pack(pady = 4)
    # e2 = Entry(topbg, show="*", width=25)
    # e2.pack(pady = 4)
    Button(topbg, text='Login', command=login).pack()

    mw.mainloop()
    