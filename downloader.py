from cgitb import enable
from doctest import OutputChecker, master
import os
from select import select
from sqlite3 import Row
from turtle import width
from webbrowser import get
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter
import customtkinter
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    # Konfigurace výšky a šířky hlavního okna
    WIDTH = 780
    HEIGHT = 350

    def __init__(self):
        super().__init__()

        # Okrajové informace (Nízev okna, favicona, etc...)
        self.iconbitmap("./img/favicon.ico")
        self.title("YouTube Downloader")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.vypnout) 


        # ============ Vytvoření dvou rámečků ============

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # ============ Levý rámeček ============

        # Configurace gridového rozložení (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10) 
        self.frame_left.grid_rowconfigure(5, weight=1) 
        self.frame_left.grid_rowconfigure(8, minsize=20)    
        self.frame_left.grid_rowconfigure(11, minsize=10) 

        # Název aplikace v levé části aplikace
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,text="Downloader",text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        #Tlačítko nastavení exportovací složky
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,text="Nastavení",command=self.setExportFolder)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        # Přizpůsobení tmavého a světlého téma/zbarvení aplikace
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Přizpůsobení:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")


        # ============ Pravý rámeček ============

        # Configurace gridového rozložení (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=0)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")


        # ============ Info rámečku ============

        # Configurace gridového rozložení (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        # Horní "displej" errorů + názvu stahovaného videa
        videoName = "Název"
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,text=videoName,height=30,corner_radius=6,fg_color=("white", "#202020"),justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)


        # ============ Pravý rámeček ============

        # Přepínání exportovacího módu (radiobuttonami)
        self.radio_var = tkinter.IntVar(value=0)

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,variable=self.radio_var,text="Video & Audio",value=0)
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=5, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,variable=self.radio_var,text="Pouze Video",value=1)
        self.radio_button_2.grid(row=1, column=1, pady=10, padx=5, sticky="n")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,variable=self.radio_var,text="Pouze Audio",value=2)
        self.radio_button_3.grid(row=1, column=2, pady=10, padx=5, sticky="n")

        # Řádka pro kopírování odkazu videa
        self.entry = customtkinter.CTkEntry(master=self.frame_right,width=120,placeholder_text="Odkaz videa")
        self.entry.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        # Tlačítko pro exportování zadaného linku v řádce
        self.button_5 = customtkinter.CTkButton(master=self.frame_right,text="Exportovat",border_width=2,fg_color=None,command=self.exportLink)
        self.button_5.grid(row=2, column=2, columnspan=1, pady=10, padx=10, sticky="we")


        # ============ Defaultní nastavení aplikace ============
        self.optionmenu_1.set("Dark")



    # ============ Funkce pro aplikaci ============
    
    # Otevření složkového dialogu pro vybrání místa stahování exportovaných videí
    def setExportFolder(self):
        cesta = open('./cesta.txt', 'r+')
        if os.path.getsize("./cesta.txt") < 1:
            self.export_slozka = filedialog.askdirectory(initialdir="C:/", title="Vyber exportovací složku")
        else:
            self.export_slozka = filedialog.askdirectory(initialdir=cesta, title="Vyber exportovací složku")
            cesta.truncate(0)
        cesta.write(self.export_slozka)
        cesta.close()

    # Exportování vložené URL videa
    def exportLink(self):
        if os.path.getsize("./cesta.txt") < 1: # Pokud textový soubor s cestou k exportovací složce je prázdný, ukáže se error a vyzve uživatele k vybrání této složky
            self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,text="Neplatná exportovací složka!",height=30,corner_radius=6,fg_color=("white", "#997103"),justify=tkinter.LEFT)
            self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)
            messagebox.showerror('Neplatná exportovací složka', 'Před exportováním určete složku, do které se budou stahovat soubory!')
            cesta = open('./cesta.txt', 'r+')
            self.export_slozka = filedialog.askdirectory(initialdir="C:/", title="Vyber exportovací složku")
            cesta.write(self.export_slozka)
            cesta.close()
        else: # Pokud je ale vše v pořádku, pokračuje se dále
            odkaz = self.entry.get()
            try:
                yt = YouTube(odkaz)
            except Exception: # Pokud zadaný odkaz není v požadovaném formátu vyvolá se chyba, která se ukáže na hlavním displeji nahoře v aplikaci
                self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,text="Video nelze zpracovat, zkuste jiné",height=30,corner_radius=6,fg_color=("white", "#990303"),justify=tkinter.LEFT)
                self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)
            else: # Pokud zadaný odkaz je v pořádku pokračuje se dále
                videoName = yt.title
                self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,text=videoName,height=30,corner_radius=6,fg_color=("white", "#202020"),justify=tkinter.LEFT)
                self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)

                # Podmínky pro určení filtrace
                if self.radio_var.get() == 0:
                    videa = yt.streams.all()
                elif self.radio_var.get() == 1:
                    videa = yt.streams.filter(only_video=True)
                elif self.radio_var.get() == 2:
                    videa = yt.streams.filter(only_audio=True)
                else:
                    videa = yt.streams.all()

                vid = list(enumerate(videa))
                self.cmb = ttk.Combobox(master=self.frame_right, value=vid, width=180, height=50)
                self.cmb.grid(row=3, column=0, columnspan=4, pady=30, padx=10)
                self.button_6 = customtkinter.CTkButton(master=self.frame_right,text="Stáhnout",border_width=2,height=20,fg_color=None,command=self.stahnouVideo)
                self.button_6.grid(row=4, column=0, columnspan=4, pady=10, padx=10, sticky="we")
    
    # Stáhnutí vybraného streamu
    def stahnouVideo(self):
        odkaz = self.entry.get()
        yt = YouTube(odkaz)

        # Podmínky pro určení filtrace
        if self.radio_var.get() == 0:
            videa = yt.streams.all()
        elif self.radio_var.get() == 1:
            videa = yt.streams.filter(only_video=True)
        elif self.radio_var.get() == 2:
            videa = yt.streams.filter(only_audio=True)
        else:
            videa = yt.streams.all()

        cesta_exportu = open('./cesta.txt', 'r')
        strm = self.cmb.current() # Určení indexu zvoleného streamu integerem (číslem)
        videa[strm].download(cesta_exportu.read()) # Stažení videa určitého streamu to vybrané složky exportu
        cesta_exportu.close()
        
    # Změna tématu/zbarvení aplikace
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Funkce pro vypnutí aplikace
    def vypnout(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()