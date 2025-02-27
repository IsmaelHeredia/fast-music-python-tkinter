#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fast Music 1.0
# Written by Ismael Heredia
# python -m pip install ttkbootstrap
# pip install python-vlc
# pip install PyDrive

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from PIL import Image, ImageTk

from pathlib import Path

import os
#os.add_dll_directory(os.getcwd())

from forms import formCancion, formVideo, formConfiguracion, formEstacion, formSincronizacion, formDescargas

import sys

import ctypes

MUSICTK_DB = "musictk.db"

from database import migrate, get_session

def ocultar_ventana():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def cargarEstilos():

    styles = ttk.Style()

    styles.configure('TButton', font="-size 14")
    styles.configure('TLabel', font="-size 14")

    styles.configure('Config.TLabel', font="-size 12")
    styles.configure('Config.TEntry', font=('sans-serif', 30))

    styles.configure('TNotebook.Tab', font="-size 12")

    styles.configure('Playlist.Treeview.Heading', font=(None, 16), background = "#4891D8")
    styles.configure('Playlist.Treeview', font=(None, 14), rowheight = 40, background="#343A40", fieldbackground="#343A40")

    styles.layout('Playlist.Treeview.Row',
        [('Treeitem.row', {'sticky': 'nswe'}),
        ('Treeitem.image', {'side': 'left', 'sticky': 'e'})])
    styles.map('Playlist.Treeview', background=[('selected', '#32465A')])
    
    styles.configure('Songs.Treeview.Heading', font=(None, 16))
    styles.configure('Songs.Treeview', font=(None, 14), rowheight = 40)
    styles.map('Songs.Treeview', background=[('selected', '#32465A')])

    styles.configure('Videos.Treeview.Heading', font=(None, 16))
    styles.configure('Videos.Treeview', font=(None, 14), rowheight = 40)
    styles.map('Videos.Treeview', background=[('selected', '#32465A')])

    styles.configure('Stations.Treeview.Heading', font=(None, 16))
    styles.configure('Stations.Treeview', font=(None, 14), rowheight = 35)
    styles.map('Stations.Treeview', background=[('selected', '#32465A')])

    styles.configure('Files.Treeview.Heading', font=(None, 16))
    styles.configure('Files.Treeview', font=(None, 14), rowheight = 35)
    styles.map('Files.Treeview', background=[('selected', '#32465A')])

    styles.configure('Descargas.TRadiobutton', background='#4E5D6C', font=(None, 14))

class Dashboard(ttk.Window):

    style = {"background": '#4e5d6c'}

    def __init__(self, *args, **kwargs):

        super().__init__(themename='superhero')

        cargarEstilos()

        ico = Image.open('icons/thunder.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)

        self.geometry('1250x870')
        self.title('Fast Music 1.0 | Copyright (C) 2025 Ismael Heredia')
        self.position_center()
        self.resizable(False, False)

        self.ventana = ttk.Frame(self, bootstyle='secondary')

        self.cancionesPlaylists = None
        self.songIdColumnActive = None
        self.repeatSongMode = False

        self.objFormCancion = None
        self.objFormVideo = None
        self.objFormEstacion = None

        self.objFormConfig = None

        self.protocol("WM_DELETE_WINDOW", self.cerrarDash)

        self.ventanaActiva = 1

        iconosLista = {
            'play': 'play.png',
            'pause': 'pause.png',
            'stop': 'stop.png',
            'previous': 'previous.png',
            'next': 'next.png',
            'repeat': 'repeat.png',
            'norepeat': 'norepeat.png',
            'playlist': 'playlist.png',
            'songs': 'songs.png',
            'videos': 'videos.png',
            'stations': 'stations.png',
            'downloads': 'downloads.png',
            'sync': 'sync.png',
            'settings': 'settings.png',
            'about': 'about.png',
            'logout': 'logout.png',
            'checked': 'checked.png',
            'unchecked': 'unchecked.png',
            'record-on': 'record-on.png',
            'record-off': 'record-off.png',
        }

        self.iconos = []

        imgpath = Path(__file__).parent / 'icons'
        for key, val in iconosLista.items():
            _path = imgpath / val
            self.iconos.append(ttk.PhotoImage(name=key, file=_path))

        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        _func = lambda: self.cargarMenuCanciones()
        btn = ttk.Button(
            master=buttonbar, text=' Música',
            image='songs', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        _func = lambda: self.cargarMenuVideos()
        btn = ttk.Button(
            master=buttonbar, text=' Vídeos',
            image='videos', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        _func = lambda: self.cargarMenuEstaciones()
        btn = ttk.Button(
            master=buttonbar, 
            text=' Streams', 
            image='stations', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        _func = lambda: self.cargarMenuDescargas()
        btn = ttk.Button(
            master=buttonbar, 
            text=' Descargas', 
            image='downloads', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        _func = lambda: self.cargarMenuSincronizacion()
        btn = ttk.Button(
            master=buttonbar, 
            text=' Sincronización', 
            image='sync',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        _func = lambda: self.cargarMenuConfiguracion()
        btn = ttk.Button(
            master=buttonbar, 
            text=' Configuración', 
            image='settings',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        _func = lambda: self.openAbout()
        btn = ttk.Button(
            master=buttonbar, 
            text=' About', 
            image='about',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        _func = lambda: self.cerrarDash()
        btn = ttk.Button(
            master=buttonbar, 
            text=' Salir', 
            image='logout',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        self.tvVideos = None
        self.media_canvas = None

        # Ventana por defecto

        self.cargarMenuCanciones()

    def detener_media(self):
        if(self.ventanaActiva == 1):
            if self.objFormCancion is not None:
                self.objFormCancion.stop_song()
        elif(self.ventanaActiva == 2):
            if self.objFormVideo is not None:
                self.objFormVideo.stop_video()
        elif(self.ventanaActiva == 3):
            if self.objFormEstacion is not None:
                self.objFormEstacion.stop_stream()

    def cerrarDash(self):
        self.detener_media()
        sys.exit(1)

    def openAbout(self):
        Messagebox.show_info("Nombre del programa : Fast Music\nVersion: 1.0\nAutor: Ismael Heredia", parent = self)

    def cargarMenuCanciones(self):
        self.detener_media()
        self.ventanaActiva = 1
        self.objFormCancion = formCancion.formCancion()
        self.objFormCancion.cargarMenuCanciones(self)
    
    def cargarMenuVideos(self):
        self.detener_media()
        self.ventanaActiva = 2
        self.objFormVideo = formVideo.formVideo()
        self.objFormVideo.cargarMenuVideos(self)

    def cargarMenuEstaciones(self):
        self.detener_media()
        self.ventanaActiva = 3
        self.objFormEstacion = formEstacion.formEstacion()
        self.objFormEstacion.cargarMenuEstaciones(self)

    def cargarMenuSincronizacion(self):
        self.detener_media()
        self.ventanaActiva = 4
        self.objFormSincronizacion = formSincronizacion.formSincronizacion()
        self.objFormSincronizacion.cargarMenuSincronizacion(self)

    def cargarMenuDescargas(self):
        self.detener_media()
        self.ventanaActiva = 5
        self.objFormDescargas = formDescargas.formDescargas()
        self.objFormDescargas.cargarMenuDescargas(self)

    def cargarMenuConfiguracion(self):
        self.objFormConfig = formConfiguracion.formConfiguracion()

dashboard = None

if __name__ == '__main__':

    ocultar_ventana()

    database_name = MUSICTK_DB
    
    if not os.path.exists(database_name):
        migrate()

    dashboard = Dashboard()
    dashboard.mainloop()