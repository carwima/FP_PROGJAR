from tkinter import *

mw = Tk()

mw.option_add("*Button.Background", "grey")
mw.option_add("*Button.Foreground", "white")

mw.title('ChatApp')
#You can set the geometry attribute to change the root windows size
mw.geometry("500x500") #You want the size of the app to be 500x500
mw.resizable(0, 0) #Don't allow resizing in the x or y direction

back = Frame(master=mw,bg='grey')
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=BOTH, expand=1) #Expand the frame to fill the root window

Lb = Listbox(back)
countlb = 0
Lb.pack(side = LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(back)
scrollbar.pack(side = RIGHT, fill = BOTH)

Lb.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = Lb.yview)

def getTextInput():
    result=textExample.get("1.0","end-1c")
    # print(result)
    Lb.insert(END, result)
    textExample.delete('1.0', END)

textExample=Text(master=mw, height=1)
textExample.pack()
btnRead=Button(master=mw, height=1, width=10, text="Send ", command=getTextInput)

btnRead.pack()
mw.mainloop()


