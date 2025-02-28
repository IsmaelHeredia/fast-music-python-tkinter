#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
import tkinter.font as tkfont

from ttkbootstrap.constants import *

from ttkbootstrap.dialogs.dialogs import Messagebox

import subprocess
import threading

import random, string, os

class formDescargas(object):

    def __init__(self):

        self.style = {"background": '#4e5d6c'}
        
        self.selfDash = None

        self.outputName = tk.StringVar()
        self.outputFolder = tk.StringVar()
        self.tipoCombo = ttk.StringVar(value="1")

        self.cmd = None
        self.filename_generated = None

        self.logs = []

    def update_logs(self):
        while len(self.logs) != 0:
            self.textConsole.insert("end", self.logs.pop(0))
        self.textConsole.after(100, self.update_logs)

    def executeDownload(self):
        with subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                self.textConsole.insert(END, line)
                self.textConsole.see(END)
            self.textConsole.text.configure(state="disabled")
            if self.filename_generated != None:
                if os.path.exists(self.filename_generated):
                    os.remove(self.filename_generated)
        self.textConsole.after(0, lambda: Messagebox.ok(message="Descarga completada"))

    def generate_random_name(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(5))

    def generate_filename(self, links):
        last_link = links[-1]
        filename = self.generate_random_name() + ".txt" 
        archivo = open(filename, "w")
        for link in links:
            if link != last_link:
                archivo.write(link + "\n")
            else:
                archivo.write(link)
        archivo.close()
        return filename

    def descargar(self):

        self.cmd = None
        self.filename_generated = None

        linksForm = self.linksEntry.get("1.0", ttk.END).split("\n")
        outputName = self.outputName.get()
        outputFolder = self.outputFolder.get()
        tipoCombo = int(self.tipoCombo.get())

        links = []

        for link in linksForm:
            if link != "":
                links.append(link)

        if(len(links) == 0):
            return

        option_string = None

        if tipoCombo == 1: # Canciones
            if len(links) == 1:
                option_string = "-download-song "
            else:
                self.filename_generated = self.generate_filename(links)
                option_string = "-download-songs "
        elif tipoCombo == 2: # Videos
            if len(links) == 1:
                option_string = "-download-video "
            else:
                self.filename_generated = self.generate_filename(links)
                option_string = "-download-videos "
        elif tipoCombo == 3: # Playlists de canciones
            option_string = "-download-playlist-songs "
        elif tipoCombo == 4: # Playlists de videos
            option_string = "-download-playlist-videos "

        linkTarget = None

        if(len(links) == 1):
            linkTarget = links[0]
        else:
            if(tipoCombo in (1,2)):
                linkTarget = self.filename_generated

        self.cmd = "video.py " + option_string + "\"" + linkTarget + "\""

        if outputName != "":
            self.cmd = self.cmd + " -output-name " + "\"" + outputName + "\""

        if outputFolder != "":
            self.cmd = self.cmd + " -output-folder " + "\"" + outputFolder + "\""

        print("CMD", self.cmd)

        self.textConsole.text.configure(state="normal")
        self.textConsole.delete("1.0", END)
        self.textConsole.insert(END, "[+] Ejecutando script ...\n\n")
        self.textConsole.see(END)

        new_download = threading.Thread(target=self.executeDownload, daemon=True)
        new_download.start()

    def limpiar_form(self):
        self.linksEntry.delete("1.0", END)
        self.outputName.set("")
        self.outputFolder.set("")
        self.tipoCombo.set(1)
        self.limpiar_consola()

    def limpiar_consola(self):
        self.textConsole.text.configure(state="normal")
        self.textConsole.delete("1.0", END)
        self.textConsole.insert(END, "[+] Consola habilitada\n\n")
        self.textConsole.text.configure(state="disabled")

    def cargarMenuDescargas(self, selfDash):

        self.selfDash = selfDash

        font = tkfont.Font(size=12)

        self.selfDash.option_add("*TCombobox*Listbox.font", font)

        selfDash.ventana.destroy()

        selfDash.ventana = ttk.Frame(selfDash, bootstyle='secondary')
        selfDash.ventana.pack_propagate(0)
        selfDash.ventana.pack(side='left', fill='both', expand=True)

        self.linksLabel = ttk.Label(selfDash, text="Links", **self.style)
        self.linksLabel.place(x = 50, y = 140)

        self.linksEntry = ScrolledText(selfDash, padding=5, height=5, width=61, font=(None, 16), autohide=True)
        self.linksEntry.place(x = 130, y = 90)

        self.outputNameLabel = ttk.Label(selfDash, text="Nombre", **self.style)
        self.outputNameLabel.place(x = 50, y = 280)

        self.outputNameEntry = ttk.Entry(selfDash, width=30, font=font, textvariable=self.outputName)
        self.outputNameEntry.place(x = 130, y = 280)

        self.outputFolderLabel = ttk.Label(selfDash, text="Directorio", **self.style)
        self.outputFolderLabel.place(x = 450, y = 280)

        self.outputFolderEntry = ttk.Entry(selfDash, width=36, font=font, textvariable=self.outputFolder)
        self.outputFolderEntry.place(x = 550, y = 280)

        self.tipoLabel = ttk.Label(selfDash, text="Tipo de descarga", **self.style)
        self.tipoLabel.place(x = 50, y = 360)

        self.tipoCancionCombo = ttk.Radiobutton(selfDash, text="Canciones", value=1, variable=self.tipoCombo, style="Descargas.TRadiobutton")
        self.tipoCancionCombo.place(x = 240, y = 365)

        self.tipoVideoCombo = ttk.Radiobutton(selfDash, text="Videos", value=2, variable=self.tipoCombo, style="Descargas.TRadiobutton")
        self.tipoVideoCombo.place(x = 370, y = 365)

        self.tipoPlaylistCancionCombo = ttk.Radiobutton(selfDash, text="Playlist de canciones", value=3, variable=self.tipoCombo, style="Descargas.TRadiobutton")
        self.tipoPlaylistCancionCombo.place(x = 470, y = 365)

        self.tipoPlaylistVideoCombo = ttk.Radiobutton(selfDash, text="Playlist de videos", value=4, variable=self.tipoCombo, style="Descargas.TRadiobutton")
        self.tipoPlaylistVideoCombo.place(x = 690, y = 365)

        self.textConsole = ScrolledText(selfDash, padding=5, height=10, width=94, font=(None, 16), autohide=True)
        self.textConsole.place(x = 50, y = 430)

        self.descargar_btn = ttk.Button(selfDash, text="Descargar", width=20, command=self.descargar)
        self.descargar_btn.place(x = 300, y = 780)

        self.descargar_btn = ttk.Button(selfDash, text="Limpiar", width=20, command=self.limpiar_form)
        self.descargar_btn.place(x = 680, y = 780)

        self.limpiar_consola()