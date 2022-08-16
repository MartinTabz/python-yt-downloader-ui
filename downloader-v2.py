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
import tkinter.messagebox

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 350

    def __init__(self):
        super().__init__()

        self.title("YouTube Downloade v2")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Downloader",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Nastavení",
                                                command=self.setExportFolder)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)


        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Přizpůsobení:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=0)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        videoName = "Název"

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=videoName ,
                                                   height=30,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "#202020"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)


        # ============ frame_right ============


        self.radio_var = tkinter.IntVar(value=0)

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text="Video & Audio",
                                                           value=0)
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=5, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text="Pouze Video",
                                                           value=1)
        self.radio_button_2.grid(row=1, column=1, pady=10, padx=5, sticky="n")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text="Pouze Audio",
                                                           value=2)
        self.radio_button_3.grid(row=1, column=2, pady=10, padx=5, sticky="n")





        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Odkaz videa")
        self.entry.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Exportovat",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.exportLink)
        self.button_5.grid(row=2, column=2, columnspan=1, pady=10, padx=10, sticky="we")


        # set default values
        self.optionmenu_1.set("Dark")
        # self.combobox_1.set("Vyber export")

    def setExportFolder(self):
        cesta = open('./cesta.txt', 'r+')
        if(os.path.getsize("./cesta.txt") < 1):
            self.export_slozka = filedialog.askdirectory(initialdir="C:/", title="Vyber exportovací složku")
        else:
            self.export_slozka = filedialog.askdirectory(initialdir=cesta, title="Vyber exportovací složku")
            cesta.truncate(0)
        cesta.write(self.export_slozka)
        cesta.close()

    def exportLink(self):
        odkaz = self.entry.get()
        try:
            yt = YouTube(odkaz)
        except Exception:
            self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Video nelze zpracovat, zkuste jiné" ,
                                                   height=30,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "#940020"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
            self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)
        else:
            videoName = yt.title
            self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text=videoName ,
                                                    height=30,
                                                    corner_radius=6,  # <- custom corner radius
                                                    fg_color=("white", "#202020"),  # <- custom tuple-color
                                                    justify=tkinter.LEFT)
            self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=10, pady=10)
            videa = yt.streams.all()
            vid = list(enumerate(videa))
            self.cmb = ttk.Combobox(master=self.frame_right, value=vid, width=180, height=50)
            # self.cmb.current(0)
            # self.cmb.bind("<<ComboboxSelected>>", self.getStream())
            self.cmb.grid(row=3, column=0, columnspan=4, pady=30, padx=10)
            self.button_6 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Stáhnout",
                                                border_width=2,
                                                height=20,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.stahnouVideo)
            self.button_6.grid(row=4, column=0, columnspan=4, pady=10, padx=10, sticky="we")
    
        
    # def getStream(self):
    #     print("method is called")
    #     print (self.cmb.get())

    def stahnouVideo(self):
        odkaz = self.entry.get()
        yt = YouTube(odkaz)
        videa = yt.streams.all()
        print (self.cmb.get())
        cesta_exportu = open('./cesta.txt', 'r')
        strm = self.cmb.current()
        videa[strm].download(cesta_exportu.read())
        cesta_exportu.close()
        print("Hotovo!")
        

                



    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()