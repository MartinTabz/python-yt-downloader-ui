import string
from turtle import bgcolor
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import os
from PIL import ImageTk,Image
import customtkinter

def exportovatLink():
    odkaz = input_odkazu.get()
    yt = YouTube(odkaz)
    promenynazev = yt.title
    nazevVidea = Label(obrazovka, text=promenynazev)
    nazevVidea.config(font=('./img/Roboto-Regular.ttf', 15))
    nazevVidea.grid(row=0, column=1)
    videa = yt.streams.all()
    vid = list(enumerate(videa))
    for i in vid:
        print(i)
    print()
    cesta_exportu = open('./cesta.txt', 'r')
    print()
    strm = int(input("Vyber export: "))
    videa[strm].download(cesta_exportu.read())
    cesta_exportu.close()
    print("Hotovo!")

obrazovka = Tk()
obrazovka.geometry('1200x650')
obrazovka.iconbitmap('./img/favicon.ico')
obrazovka.configure(bg='#121212')
obrazovka.resizable(0,0)
title = obrazovka.title("YouTube Downloader")

promenynazev = "Vložte odkaz na YouTube video a stiskněte exportovat"
nazevVidea = Label(obrazovka, text=promenynazev)
nazevVidea.config(font=('./img/Roboto-Regular.ttf', 15), background="#121212", foreground="White")
nazevVidea.grid(row=0, column=0)

export = Button(obrazovka, text="Exportovat", command=exportovatLink)
export.grid(row=1, column=1)

input_odkazu = Entry()
input_odkazu.config(width=50, font=('./img/Roboto-Regular.ttf', 15))
input_odkazu.grid(row=1, column=0)

def nastaveniSlozky():
    cesta = open('./cesta.txt', 'r+')
    if(os.path.getsize("./cesta.txt") == 0):
        obrazovka.export_slozka = filedialog.askdirectory(initialdir="C:/", title="Vyber exportovací složku")
    else:
        obrazovka.export_slozka = filedialog.askdirectory(initialdir=cesta, title="Vyber exportovací složku")
        cesta.truncate(0)
    cesta.write(obrazovka.export_slozka)
    cesta.close()

nastaveni_img = PhotoImage(file = "./img/nastaveni.png")
nastaveniBtn = Button(obrazovka, image = nastaveni_img, command=nastaveniSlozky)
nastaveniBtn.grid(row=0, column=1)

obrazovka.mainloop()
