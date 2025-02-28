#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import tkinter.font as tkfont
from ttkbootstrap.constants import *

from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfile
import threading
import json

from services.configurationService import ConfigurationService
from services.stationsService import StationsService

class formConfiguracion(ttk.Toplevel):

    style = {"background": '#4e5d6c'}

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.configurationService = ConfigurationService()
        self.stationsService = StationsService()

        font = tkfont.Font(size=12)

        self.geometry('900x400')
        self.title('Configuración')
        self.position_center()
        self.resizable(False, False)

        notebook = ttk.Notebook(self, bootstyle="dark", width=850, height=300)
        notebook.place(x = 10, y = 10)

        tab_multimedia = ttk.Frame(notebook)
        tab_estaciones = ttk.Frame(notebook)
        tab_sincronizacion = ttk.Frame(notebook)
        tab_descargas = ttk.Frame(notebook)

        # Cargar datos guardados

        self.config = self.configurationService.cargarConfiguracion()

        self.songs_directory = self.config["songs_directory"]
        self.videos_directory = self.config["videos_directory"]
        self.songs_directory_gd = self.config["songs_directory_gd"]
        self.songs_directory_downloads = self.config["songs_directory_downloads"]
        self.videos_directory_downloads = self.config["videos_directory_downloads"]

        # Tab de multimedia

        self.directorioCancionesMultimedia = tk.StringVar(value = self.songs_directory)
        self.directorioVideosMultimedia = tk.StringVar(value = self.videos_directory)

        self.directorioCancionesLabel = ttk.Label(tab_multimedia, text="Directorio de canciones", style='Config.TLabel')
        self.directorioCancionesLabel.place(x = 30, y = 23)

        self.directorioCancionesEntry = ttk.Entry(tab_multimedia, width=49, style='Config.TEntry', font=font, textvariable=self.directorioCancionesMultimedia)
        self.directorioCancionesEntry.place(x = 210, y = 23)

        self.seleccionarDirectorioCancionButton = ttk.Button(tab_multimedia, text="Seleccionar", command=self.cargarCarpetaCancionMultimedia)
        self.seleccionarDirectorioCancionButton.place(x = 680, y = 23)

        self.directorioVideosLabel = ttk.Label(tab_multimedia, text="Directorio de videos", style='Config.TLabel')
        self.directorioVideosLabel.place(x = 30, y = 73)

        self.directorioVideosEntry = ttk.Entry(tab_multimedia, width=49, style='Config.TEntry', font=font, textvariable=self.directorioVideosMultimedia)
        self.directorioVideosEntry.place(x = 210, y = 73)

        self.seleccionarDirectorioVideoButton = ttk.Button(tab_multimedia, text="Seleccionar", command=self.cargarCarpetaVideosMultimedia)
        self.seleccionarDirectorioVideoButton.place(x = 680, y = 73)

        self.guardarButton = ttk.Button(tab_multimedia, text="Guardar", width=15, command=self.guardarMultimedia)
        self.guardarButton.place(x = 220, y = 150)

        self.scanButton = ttk.Button(tab_multimedia, text="Escanear", width=15, command=self.escanearMultimedia)
        self.scanButton.place(x = 480, y = 150)

        # Tab de estaciones

        self.archivoJSONEstaciones = tk.StringVar()

        self.archivoImportarJSONLabel = ttk.Label(tab_estaciones, text="Archivo JSON", style='Config.TLabel')
        self.archivoImportarJSONLabel.place(x = 30, y = 23)

        self.archivoImportarJSONEntry = ttk.Entry(tab_estaciones, width=49, style='Config.TEntry', font=font, textvariable=self.archivoJSONEstaciones)
        self.archivoImportarJSONEntry.place(x = 210, y = 23)

        self.seleccionarArchivoJSONButton = ttk.Button(tab_estaciones, text="Seleccionar", command=self.seleccionarArchivoJSON)
        self.seleccionarArchivoJSONButton.place(x = 680, y = 23)

        self.importarButton = ttk.Button(tab_estaciones, text="Importar", width=15, command=self.importarArchivoJSON)
        self.importarButton.place(x = 135, y = 120)

        self.exportarButton = ttk.Button(tab_estaciones, text="Exportar", width=15, command=self.exportarArchivoJSON)
        self.exportarButton.place(x = 335, y = 120)

        self.validarButton = ttk.Button(tab_estaciones, text="Validar", width=15, command=self.validarEstaciones)
        self.validarButton.place(x = 535, y = 120)

        # Tab sincronización

        self.directorioCancionesGD = tk.StringVar(value = self.songs_directory_gd)

        self.directorioCancionesGDLabel = ttk.Label(tab_sincronizacion, text="Directorio de canciones", style='Config.TLabel')
        self.directorioCancionesGDLabel.place(x = 30, y = 23)

        self.directorioCancionesGDEntry = ttk.Entry(tab_sincronizacion, width=49, style='Config.TEntry', font=font, textvariable=self.directorioCancionesGD)
        self.directorioCancionesGDEntry.place(x = 210, y = 23)

        self.guardarGDButton = ttk.Button(tab_sincronizacion, text="Guardar", width=10, command=self.guardarSincronizacion)
        self.guardarGDButton.place(x = 690, y = 23)

        # Tab de descargas

        self.directorioCancionesYT = tk.StringVar(value = self.songs_directory_downloads)
        self.directorioVideosYT = tk.StringVar(value = self.videos_directory_downloads)

        self.directorioCancionesYTLabel = ttk.Label(tab_descargas, text="Directorio de canciones", style='Config.TLabel')
        self.directorioCancionesYTLabel.place(x = 30, y = 23)

        self.directorioCancionesYTEntry = ttk.Entry(tab_descargas, width=49, style='Config.TEntry', font=font, textvariable=self.directorioCancionesYT)
        self.directorioCancionesYTEntry.place(x = 210, y = 23)

        self.seleccionarDirectorioCancionYTButton = ttk.Button(tab_descargas, text="Seleccionar", command=self.cargarCarpetaCancionYT)
        self.seleccionarDirectorioCancionYTButton.place(x = 680, y = 23)

        self.directorioVideosYTLabel = ttk.Label(tab_descargas, text="Directorio de videos", style='Config.TLabel')
        self.directorioVideosYTLabel.place(x = 30, y = 73)

        self.directorioVideosYTEntry = ttk.Entry(tab_descargas, width=49, style='Config.TEntry', font=font, textvariable=self.directorioVideosYT)
        self.directorioVideosYTEntry.place(x = 210, y = 73)

        self.seleccionarDirectorioVideoYTButton = ttk.Button(tab_descargas, text="Seleccionar", command=self.cargarCarpetaVideosYT)
        self.seleccionarDirectorioVideoYTButton.place(x = 680, y = 73)

        self.guardarYTButton = ttk.Button(tab_descargas, text="Guardar", width=15, command=self.guardarDescargas)
        self.guardarYTButton.place(x = 340, y = 150)

        #

        notebook.add(tab_multimedia, text="Multimedia")
        notebook.add(tab_estaciones, text="Streams")
        notebook.add(tab_sincronizacion, text="Sincronización")
        notebook.add(tab_descargas, text="Descargas")

    def cargarCarpetaCancionMultimedia(self):
        path = askdirectory(title="Seleccione carpeta de canciones", parent = self)
        if path:
            self.directorioCancionesMultimedia.set(path)

    def cargarCarpetaVideosMultimedia(self):
        path = askdirectory(title="Seleccione carpeta de videos", parent = self)
        if path:
            self.directorioVideosMultimedia.set(path)

    def guardarMultimedia(self):
        songs_directory = self.directorioCancionesMultimedia.get()
        videos_directory = self.directorioVideosMultimedia.get()
        if songs_directory != "" and videos_directory != "":
            self.configurationService.fijarDirectoriosMultimedia(songs_directory, videos_directory)
            Messagebox.ok(message="Los directorios fueron guardados correctamente", parent = self)
        else:
            Messagebox.ok(message="Complete los datos", parent = self)

    def iniciar_escaneo(self):
        escaneoCanciones = self.configurationService.scanSongs()
        escaneoVideos = self.configurationService.scanVideos()
        mensaje = None
        if escaneoCanciones == True and escaneoVideos == True:
            mensaje = "El escaneo finalizo correctamente"
        elif escaneoCanciones == False:
            mensaje = "Ocurrió un error escaneando las canciones"
        elif escaneoVideos == False:
            mensaje = "Ocurrió un error escaneando los videos"
        self.after(1000, self.finalizar_escaneo, mensaje)

    def finalizar_escaneo(self, mensaje):
        self.scanButton.config(state=NORMAL)
        self.scanButton.config(text="Escanear")
        Messagebox.ok(message=mensaje, parent = self)

    def escanearMultimedia(self):
        self.scanButton.config(text="Escaneando")
        self.scanButton.config(state=DISABLED)
        threadScan = threading.Thread(target=self.iniciar_escaneo)
        threadScan.start()
    
    def seleccionarArchivoJSON(self):
        filename = askopenfilename(title="", filetypes=[("JSON files","*.json")], parent = self)
        if filename:
            self.archivoJSONEstaciones.set(filename)

    def iniciar_importacion(self):
        json_file = self.archivoJSONEstaciones.get()
        estadoImportacion = self.stationsService.importFile(json_file)
        mensaje = None
        if estadoImportacion == True:
            mensaje = "La importación se ejecutó correctamente"
        else:
            mensaje = "Ocurrió un error en la importación"
        self.after(1000, self.finalizar_importacion, mensaje)

    def finalizar_importacion(self, mensaje):
        self.importarButton.config(state=NORMAL)
        self.importarButton.config(text="Importar")
        Messagebox.ok(message=mensaje, parent = self)

    def importarArchivoJSON(self):
        json_file = self.archivoJSONEstaciones.get()
        if json_file != "":
            self.importarButton.config(text="Importando")
            self.importarButton.config(state=DISABLED)
            threadImport = threading.Thread(target=self.iniciar_importacion)
            threadImport.start()
        else:
            Messagebox.ok(message="Seleccione el archivo JSON", parent = self)

    def exportarArchivoJSON(self):
        files_extensions = [('JSON File', '*.json')]
        file_exported = asksaveasfile(filetypes = files_extensions, defaultextension = files_extensions) 
        if file_exported:
            stationsList = []
            stations = self.stationsService.list()
            for station in stations:
                stationsList.append({
                    "id": station["id"],
                    "name": station["name"],
                    "link": station["link"],
                    "categories": station["categories"]
                })
            with open(file_exported.name, "w") as outfile:
                json.dump(stationsList, outfile, indent=4)
            Messagebox.ok(message="La exportación se ejecutó correctamente", parent = self)

    def iniciar_validacion(self):
        estadoValidacion = self.stationsService.validate()
        mensaje = None
        if estadoValidacion == True:
            mensaje = "La validación se ejecutó correctamente"
        else:
            mensaje = "Ocurrió un error en la importación"
        self.after(1000, self.finalizar_validacion, mensaje)

    def finalizar_validacion(self, mensaje):
        self.validarButton.config(state=NORMAL)
        self.validarButton.config(text="Validar")
        Messagebox.ok(message=mensaje, parent = self)

    def validarEstaciones(self):
        self.validarButton.config(text="Validando")
        self.validarButton.config(state=DISABLED)
        threadValidate = threading.Thread(target=self.iniciar_validacion)
        threadValidate.start()

    def guardarSincronizacion(self):
        songs_directory_gd = self.directorioCancionesGD.get()
        if songs_directory_gd != "":
            self.configurationService.fijarDirectorioGD(songs_directory_gd)
            Messagebox.ok(message="El directorio de Google Drive fue guardado correctamente", parent = self)
        else:
            Messagebox.ok(message="Complete los datos", parent = self)

    def cargarCarpetaCancionYT(self):
        path = askdirectory(title="Seleccione carpeta de canciones", parent = self)
        if path:
            self.directorioCancionesYT.set(path)

    def cargarCarpetaVideosYT(self):
        path = askdirectory(title="Seleccione carpeta de videos", parent = self)
        if path:
            self.directorioVideosYT.set(path)

    def guardarDescargas(self):
        songs_directory_downloads = self.directorioCancionesYT.get()
        videos_directory_downloads =self.directorioVideosYT.get()
        if songs_directory_downloads != "" and videos_directory_downloads != "":
            self.configurationService.fijarDirectoriosDescargas(songs_directory_downloads, videos_directory_downloads)
            Messagebox.ok(message="Los directorios fueron guardados correctamente", parent = self)
        else:
            Messagebox.ok(message="Complete los datos", parent = self)