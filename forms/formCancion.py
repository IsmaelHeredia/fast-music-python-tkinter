#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk

import vlc

from datetime import timedelta

from forms.formPlaylists import formPlaylists

from services.songsService import SongsService
from services.historyService import HistoryService

class formCancion(object):

    def __init__(self):

        self.style = {"background": '#4e5d6c'}
        
        self.songsService = SongsService()
        self.historyService = HistoryService()

        self.iniciarPlayer()

        self.reproducirCancion_btn = None

        self.cancionesPlaylists = None
        self.songIdColumnActive = None
        self.repeatVideoMode = False

        self.selfDash = None

        self.repeatSongMode = False

        self.playlistsSongsSaved = self.historyService.getPlaylistsSongsSaved()

    def iniciarPlayer(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_player.audio_set_volume(100)
        self.current_file = None
        self.playing_video = False
        self.video_paused = False

    def get_duration_string(self):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
            return total_duration_str
        return "00:00:00"

    def next(self):
        if self.playing_video:
            ids = []
            for id in self.tvCanciones.get_children():
                ids.append(id)
            currentIndex = ids.index(self.songIdColumnActive)
            index = currentIndex + 1
            nextMedia = None
            if currentIndex == len(ids) - 1:
                nextMedia = ids[0]
            else:
                nextMedia = ids[index]
            self.stop_song()
            self.disableFocusSongTable()
            self.songIdColumnActive = nextMedia
            item = self.tvCanciones.item(nextMedia)
            values = item['values']
            nombreCancion = values[0]
            playlistCancion = values[2]
            data = self.songsService.findSongByName(nombreCancion, playlistCancion)
            self.current_file = data['fullpath']
            self.play_song()
            self.enableFocusSongTable()

    def previous(self):
        if self.playing_video:
            ids = []
            for id in self.tvCanciones.get_children():
                ids.append(id)
            currentIndex = ids.index(self.songIdColumnActive)
            index = currentIndex - 1
            nextMedia = None
            if currentIndex == 0:
                nextMedia = ids[len(ids) - 1]
            else:
                nextMedia = ids[index]
            self.stop_song()
            self.disableFocusSongTable()
            self.songIdColumnActive = nextMedia
            item = self.tvCanciones.item(nextMedia)
            values = item['values']
            nombreCancion = values[0]
            playlistCancion = values[2]
            data = self.songsService.findSongByName(nombreCancion, playlistCancion)
            self.current_file = data['fullpath']
            self.play_song()
            self.enableFocusSongTable()

    def play_song(self):
        if self.current_file is not None:
            if not self.playing_video:

                self.tiempoActualLabel.config(text = "00:00:00")
                self.tiempoTotalLabel.config(text = self.get_duration_string())

                media = self.instance.media_new(self.current_file)

                self.media_player.set_media(media)

                self.media_player.play()

                self.playing_video = True

                self.reproducirCancion_btn.config(image = 'pause')

                self.controlar_estado_cancion()

            else:
                if self.video_paused:
                    self.media_player.play()
                    self.video_paused = False
                    self.reproducirCancion_btn.config(image = 'pause')
                else:
                    self.media_player.pause()
                    self.video_paused = True
                    self.reproducirCancion_btn.config(image = 'play')

    def stop_song(self, isRepeat = False):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False
            self.tiempoTotalLabel.config(text="00:00:00")
            self.tiempoActualLabel.config(text="00:00:00")
            self.barraProgreso.set(0)

            if self.songIdColumnActive is not None and isRepeat == False:
                self.tvCanciones.item(self.songIdColumnActive, tags=['unselected'])

    def format_time(self, value):
        seconds, milliseconds = divmod(value, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return ("%02i:%02i:%02i" % (hours, minutes, seconds))

    def controlar_estado_cancion(self):
        
        if self.playing_video:

            total_duration = self.media_player.get_length()
            current_time = self.media_player.get_time()

            try:
                progress_percentage = (current_time / total_duration) * 100
            except ZeroDivisionError:
                progress_percentage = 0

            self.barraProgreso.set(progress_percentage)

            total_duration_str = self.format_time(total_duration)
            current_time_str = self.format_time(current_time)

            self.tiempoTotalLabel.config(text=total_duration_str)
            self.tiempoActualLabel.config(text=current_time_str)

            if (self.media_player.get_state() == vlc.State.Ended) and (current_time != 0):
                if self.repeatSongMode == False:
                    self.next()
                else:
                    self.stop_song(True)
                    self.play_song()

        self.selfDash.after(1000, self.controlar_estado_cancion)

    def handleProgresoPosition(self, event):
        if self.playing_video:
            value = (event.x / event.widget.winfo_width()) * 100
            total_duration = self.media_player.get_length()
            position = int((float(value) / 100) * total_duration)
            self.media_player.set_time(position)

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

    def loadPlaylistsSongs(self):
        self.cancionesPlaylists = formPlaylists()
        self.cancionesPlaylists.setDashboard(self)
        self.cancionesPlaylists.setMediaType(1)

    def enableFocusSongTable(self):
        if self.songIdColumnActive is not None:
            self.tvCanciones.item(self.songIdColumnActive, tags=['selected'])
        
    def disableFocusSongTable(self):
        if self.songIdColumnActive is not None:
            self.tvCanciones.item(self.songIdColumnActive, tags=['unselected'])

    def handleClickLoadSong(self, event):

        self.stop_song()

        self.disableFocusSongTable()

        itemFocus = self.tvCanciones.focus()

        item = self.tvCanciones.item(itemFocus)

        itemValues = item['values']

        nombreCancion = itemValues[0]
        playlistCancion = itemValues[2]
        
        data = self.songsService.findSongByName(nombreCancion, playlistCancion)

        self.current_file = data['fullpath']
        self.play_song()

        self.tvCanciones.selection_remove(self.tvCanciones.selection())

        self.songIdColumnActive = self.tvCanciones.identify_row(event.y)

        self.enableFocusSongTable()

    def cargarTabla(self):
        for playlist_id in self.playlistsSongsSaved:
            songsList = self.songsService.getSongsByIdPlaylist(playlist_id)
            for song in songsList:
                title = song["title"]
                duration = song["duration"]
                playlist = song["playlist_name"]
                self.tvCanciones.insert("","end",values=(title, duration, playlist), tags='unselected')

    def cargarMenuCanciones(self, selfDash):

        self.selfDash = selfDash

        self.ventanaActiva = 1

        valorProgreso = 0
        valorVolumen = 100

        selfDash.ventana.destroy()

        selfDash.ventana = ttk.Frame(selfDash, bootstyle='secondary')
        selfDash.ventana.pack_propagate(0)
        selfDash.ventana.pack(side='left', fill='both', expand=True)

        self.tvCanciones = ttk.Treeview(
            selfDash.ventana,
            bootstyle='dark',
            show='headings',
            height=13,
            style='Songs.Treeview',
        )
        
        self.tvCanciones.configure(columns=(
            'Título', 'Duración', 'Playlist'
        ))

        self.tvCanciones.column('Título', width=524, stretch=True, anchor='center')
        self.tvCanciones.column('Duración', width=150, stretch=True, anchor='center')
        self.tvCanciones.column('Playlist', width=500, stretch=True, anchor='center')
                
        for col in self.tvCanciones['columns']:
            self.tvCanciones.heading(col, text=col.title(), anchor='center')

        self.tvCanciones.place(x = 10, y = 10)
        
        scrollSongs = ttk.Scrollbar(selfDash.ventana, orient="vertical", bootstyle='secondary', command=self.tvCanciones.yview)
        scrollSongs.place(x = 1200, y = 13, height = 550)

        self.tvCanciones.configure(yscrollcommand=scrollSongs.set)

        self.tvCanciones.tag_configure('selected', background='#526170')
        self.tvCanciones.tag_configure('unselected', background='#32465A')

        self.tvCanciones.bind("<Double-Button-1>", self.handleClickLoadSong)
        self.tvCanciones.unbind("<Button-1>")

        self.tiempoActualLabel = ttk.Label(selfDash.ventana, text='00:00:00', **self.style)
        self.tiempoActualLabel.place(x = 35, y = 600)

        style = ttk.Style()
        style.configure('Custom.Horizontal.TScale', background='#4e5d6c')

        self.barraProgreso = ttk.Scale(
            master=selfDash.ventana, 
            bootstyle="info",
            from_=0,
            to=100,
            length=900,
            value=valorProgreso,
            style='Custom.Horizontal.TScale',
        )
        
        self.barraProgreso.place(x = 150, y = 606)

        self.barraProgreso.bind("<Button-1>", self.handleProgresoPosition)
        self.barraProgreso.bind("<ButtonRelease>", self.handleProgresoPosition)

        self.tiempoTotalLabel = ttk.Label(selfDash.ventana, text='00:00:00', **self.style)
        self.tiempoTotalLabel.place(x= 1080, y = 600)

        buttonIcon_style = ttk.Style()
        buttonIcon_style.configure('ButtonIcon.TButton', font="-size 33", color = 'white')

        buttonIcon2_style = ttk.Style()
        buttonIcon2_style.configure('ButtonIcon2.TButton', font="-size 33", color = 'white')

        cargarCancionAnterior_btn = ttk.Button(
            master=selfDash.ventana,
            image='previous',
            command=self.previous,
            style='ButtonIcon.TButton'
        )
        cargarCancionAnterior_btn.place(x = 200, y = 700)

        self.reproducirCancion_btn = ttk.Button(
            master=selfDash.ventana,
            image='play', 
            command=self.play_song,
            style='ButtonIcon.TButton'
        )
        self.reproducirCancion_btn.place(x = 300, y = 700)

        cargarSiguienteCancion_btn = ttk.Button(
            master=selfDash.ventana,
            image='next',
            command=self.next,
            style='ButtonIcon.TButton'
        )
        cargarSiguienteCancion_btn.place(x = 400, y = 700)

        detenerCancion_btn = ttk.Button(
            master=selfDash.ventana,
            image='stop',
            command=self.stop_song,
            style='ButtonIcon.TButton'
        )
        detenerCancion_btn.place(x = 500, y = 700)      

        self.modoRepetir_btn = ttk.Button(
            master=selfDash.ventana,
            image='norepeat',
            style='ButtonIcon2.TButton',
            command=self.repeatMode,
        )
        self.modoRepetir_btn.place(x = 600, y = 700)

        cargarPlaylist_btn = ttk.Button(
            master=selfDash.ventana,
            image='playlist',
            command=self.loadPlaylistsSongs,
            style='ButtonIcon2.TButton',
        )
        cargarPlaylist_btn.place(x = 690, y = 700)

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