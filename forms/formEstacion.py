#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText

import vlc

from services.stationsService import StationsService

import threading

from ttkbootstrap.constants import *

import requests

class formEstacion(object):

    def __init__(self):

        self.style = {"background": '#4e5d6c'}
        
        self.stationsService = StationsService()

        self.iniciarPlayer()

        self.reproducirEstacion_btn = None

        self.cancionesPlaylists = None
        self.stationIdColumnActive = None
        self.repeatVideoMode = False

        self.prevSong = None

        self.selfDash = None

        self.stationsList = []

        self.consoleStatus = False
        self.textConsole = None
        self.textoConsolaHabilitada = "[+] Registro de streams habilitado"
        self.textoConsolaDesabilitada = "[+] Registro de streams desabilitado"

    def iniciarPlayer(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_player.audio_set_volume(100)
        self.current_link = None
        self.playing_video = False
        self.video_paused = False

    def next(self):
        if self.playing_video:
            ids = []
            for id in self.tvEstaciones.get_children():
                ids.append(id)
            currentIndex = ids.index(self.stationIdColumnActive)
            index = currentIndex + 1
            nextMedia = None
            if currentIndex == len(ids) - 1:
                nextMedia = ids[0]
            else:
                nextMedia = ids[index]
            self.stop_stream()
            self.disableFocusStationTable()
            self.stationIdColumnActive = nextMedia
            item = self.tvEstaciones.item(nextMedia)
            values = item['values']
            nombreEstacion = values[0]
            data = self.stationsService.findStationByName(nombreEstacion)
            self.current_link = data['link']
            self.consola_por_defecto()
            self.play_stream()
            self.enableFocusStationTable()

    def previous(self):
        if self.playing_video:
            ids = []
            for id in self.tvEstaciones.get_children():
                ids.append(id)
            currentIndex = ids.index(self.stationIdColumnActive)
            index = currentIndex - 1
            nextMedia = None
            if currentIndex == 0:
                nextMedia = ids[len(ids) - 1]
            else:
                nextMedia = ids[index]
            self.stop_stream()
            self.disableFocusStationTable()
            self.stationIdColumnActive = nextMedia
            item = self.tvEstaciones.item(nextMedia)
            values = item['values']
            nombreEstacion = values[0]
            data = self.stationsService.findStationByName(nombreEstacion)
            self.current_link = data['link']
            self.consola_por_defecto()
            self.play_stream()
            self.enableFocusStationTable()

    def consola_por_defecto_habilitada(self):
        self.textConsole.text.configure(state="normal")
        self.textConsole.delete("1.0", END)
        self.textConsole.insert(END, self.textoConsolaHabilitada + "\n")
        self.textConsole.text.configure(state="disabled")

    def consola_por_defecto_dehabilitada(self):
        self.textConsole.text.configure(state="normal")
        self.textConsole.delete("1.0", END)
        self.textConsole.insert(END, self.textoConsolaDesabilitada + "\n")
        self.textConsole.text.configure(state="disabled")

    def limpiar_consola(self):
        if self.consoleStatus == True:
            self.consola_por_defecto_habilitada()
        elif self.consoleStatus == False:
            self.consola_por_defecto_dehabilitada()

    def escribir_consola(self, texto):
        self.textConsole.text.configure(state="normal")
        self.textConsole.insert(END, texto + "\n")
        self.textConsole.text.configure(state="disabled")

    def actualizar_canciones(self):
        m = self.media.get_meta(12)
        if m != self.prevSong and m is not None:
            self.prevSong = m
            self.escribir_consola("Reproducción actual : %s" % (m,))

    def iniciar_consola(self):
        if self.playing_video:
            self.actualizar_canciones()
            self.selfDash.after(1000, self.iniciar_consola)

    def obtener_headers(self, url):
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                self.procesar_headers(response.headers)
            else:
                raise requests.RequestException(f"Error al cargar headers con HEAD {response.status_code}")
        except requests.RequestException:
            try:
                response = requests.get(url, stream=True, timeout=5)
                if response.status_code == 200:
                    self.procesar_headers(response.headers)
                response.close()
            except requests.RequestException as e:
                self.escribir_consola(f"Error al cargar headers: {e}")
                
    def procesar_headers(self, headers):
        self.escribir_consola("Información de transmisión:")
        for key, value in headers.items():
            self.escribir_consola(f"{key}: {value}")

    def play_stream(self):
        if self.current_link is not None:
            if not self.playing_video:
                self.limpiar_consola()
                if self.consoleStatus == True:
                    headers_thread = threading.Thread(target=self.obtener_headers, args=(self.current_link,))
                    headers_thread.start()

                self.media = self.instance.media_new(self.current_link)

                self.media.get_mrl()

                self.media_player.set_media(self.media)

                self.media_player.play()

                self.playing_video = True

                self.reproducirEstacion_btn.config(image = 'stop')

                if self.consoleStatus == True:
                    self.threadConsole = threading.Thread(target=self.iniciar_consola)
                    self.threadConsole.start()
            else:
                self.reproducirEstacion_btn.config(image = 'play')
                self.stop_stream()
                self.consola_por_defecto_habilitada()

    def stop_stream(self, isRepeat = False):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False
            if self.stationIdColumnActive is not None and isRepeat == False:
                self.tvEstaciones.item(self.stationIdColumnActive, tags=['unselected'])

    def handleVolumenSlider(self, event):
        if self.playing_video:
            value = round((event.x / event.widget.winfo_width()) * 100)
            self.barraVolumen.set(value)
            self.media_player.audio_set_volume(value)

    def repeatMode(self):
        if self.repeatSongMode == False:
            self.modoRepetir_btn.config(image = 'repeat')
            self.repeatSongMode = True
        else:
            self.modoRepetir_btn.config(image = 'norepeat')
            self.repeatSongMode = False

    def enableFocusStationTable(self):
        if self.stationIdColumnActive is not None:
            self.tvEstaciones.item(self.stationIdColumnActive, tags=['selected'])
        
    def disableFocusStationTable(self):
        if self.stationIdColumnActive is not None:
            self.tvEstaciones.item(self.stationIdColumnActive, tags=['unselected'])

    def handleClickLoadStation(self, event):

        self.stop_stream()

        self.disableFocusStationTable()

        itemFocus = self.tvEstaciones.focus()

        item = self.tvEstaciones.item(itemFocus)

        itemValues = item['values']

        nombreEstacion = itemValues[0]
        
        data = self.stationsService.findStationByName(nombreEstacion)

        self.current_link = data['link']
        self.play_stream()

        self.tvEstaciones.selection_remove(self.tvEstaciones.selection())

        self.stationIdColumnActive = self.tvEstaciones.identify_row(event.y)

        self.enableFocusStationTable()
    
    def turnConsole(self):
        if self.consoleStatus == True:
            self.consoleStatus = False
            self.controlConsola_btn.config(image = 'record-on')
            self.limpiar_consola()
        elif self.consoleStatus == False:
            self.consoleStatus = True
            self.controlConsola_btn.config(image = 'record-off')
            self.limpiar_consola()

    def cargarTabla(self):
        self.stationsList = self.stationsService.list()
        for station in self.stationsList:
            name = station["name"]
            link = station["link"]
            categories = station["categories"]
            self.tvEstaciones.insert("","end",values=(name, link, categories), tags="unselected")

    def cargarMenuEstaciones(self, selfDash):

        self.selfDash = selfDash

        self.ventanaActiva = 1

        valorVolumen = 100

        selfDash.ventana.destroy()

        selfDash.ventana = ttk.Frame(selfDash, bootstyle='secondary')
        selfDash.ventana.pack_propagate(0)
        selfDash.ventana.pack(side='left', fill='both', expand=True)

        self.tvEstaciones = ttk.Treeview(
            selfDash.ventana,
            bootstyle='dark',
            show='headings',
            height=13,
            style='Stations.Treeview',
        )
        
        self.tvEstaciones.configure(columns=(
            'Nombre', 'Link', 'Categorias'
        ))

        self.tvEstaciones.column('Nombre', width=524, stretch=True, anchor='center')
        self.tvEstaciones.column('Link', width=400, stretch=True, anchor='center')
        self.tvEstaciones.column('Categorias', width=246, stretch=True, anchor='center')
                
        for col in self.tvEstaciones['columns']:
            self.tvEstaciones.heading(col, text=col.title(), anchor='center')

        self.tvEstaciones.place(x = 10, y = 10)
        
        scrollStations = ttk.Scrollbar(selfDash.ventana, orient="vertical", bootstyle='secondary', command=self.tvEstaciones.yview)
        scrollStations.place(x = 1200, y = 13, height = 493)

        self.tvEstaciones.configure(yscrollcommand=scrollStations.set)

        self.tvEstaciones.tag_configure('selected', background='#526170')
        self.tvEstaciones.tag_configure('unselected', background='#32465A')

        self.tvEstaciones.bind("<Double-Button-1>", self.handleClickLoadStation)
        self.tvEstaciones.unbind("<Button-1>")

        self.textConsole = ScrolledText(selfDash, padding=5, height=5, width=96, font=(None, 16), autohide=True, state="disabled")
        self.textConsole.place(x = 10, y = 580)

        buttonIcon_style = ttk.Style()
        buttonIcon_style.configure('ButtonIcon.TButton', font="-size 33", color = 'white')

        buttonIcon2_style = ttk.Style()
        buttonIcon2_style.configure('ButtonIcon2.TButton', font="-size 33", color = 'white')

        cargarEstacionAnterior_btn = ttk.Button(
            master=selfDash.ventana,
            image='previous',
            command=self.previous,
            style='ButtonIcon.TButton'
        )
        cargarEstacionAnterior_btn.place(x = 200, y = 700)

        self.reproducirEstacion_btn = ttk.Button(
            master=selfDash.ventana,
            image='play', 
            command=self.play_stream,
            style='ButtonIcon.TButton'
        )
        self.reproducirEstacion_btn.place(x = 300, y = 700)

        cargarSiguienteEstacion_btn = ttk.Button(
            master=selfDash.ventana,
            image='next',
            command=self.next,
            style='ButtonIcon.TButton'
        )
        cargarSiguienteEstacion_btn.place(x = 400, y = 700)

        self.controlConsola_btn = ttk.Button(
            master=selfDash.ventana,
            image='record-on',
            command=self.turnConsole,
            style='ButtonIcon.TButton'
        )
        self.controlConsola_btn.place(x = 500, y = 700)    

        style = ttk.Style()
        style.configure('Custom.Horizontal.TScale', background='#4e5d6c')

        self.barraVolumen = ttk.Scale(
            master=selfDash.ventana, 
            bootstyle="info",
            from_=0,
            to=100,
            length=250,
            value=valorVolumen,
            style='Custom.Horizontal.TScale'
        )
        self.barraVolumen.place(x = 860, y = 725)

        self.barraVolumen.bind("<Button-1>", self.handleVolumenSlider)
        self.barraVolumen.bind("<ButtonRelease>", self.handleVolumenSlider)

        self.cargarTabla()

        self.limpiar_consola()