#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk

import vlc

from datetime import timedelta

from forms.formPlaylists import formPlaylists

from services.videosService import VideosService
from services.playlistsService import PlaylistsService
from services.historyService import HistoryService

class formVideo(object):

    def __init__(self):

        self.style = {"background": '#4e5d6c'}
        
        self.playlistsService = PlaylistsService()
        self.videosService = VideosService()
        self.historyService = HistoryService()

        self.iniciarPlayer()

        self.reproducirCancion_btn = None

        self.cancionesPlaylists = None
        self.videoIdColumnActive = None
        self.repeatVideoMode = False

        self.selfDash = None

        self.media_canvas = None

        self.videoIdActive = None

        self.videosList = []

        self.playlistsVideosSaved = self.historyService.getPlaylistsVideosSaved()

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
            for id in self.tvVideos.get_children():
                ids.append(id)
            currentIndex = ids.index(self.videoIdColumnActive)
            index = currentIndex + 1
            nextMedia = None
            if currentIndex == len(ids) - 1:
                nextMedia = ids[0]
            else:
                nextMedia = ids[index]
            print("index", currentIndex)
            print("next", nextMedia)
            self.stop_video()
            self.disableFocusVideoTable()
            self.videoIdColumnActive = nextMedia
            item = self.tvVideos.item(nextMedia)
            values = item['values']
            nombreVideo = values[0]
            playlistVideo = values[2]
            data = self.videosService.findVideoByName(nombreVideo, playlistVideo)
            self.current_file = data['fullpath']
            self.play_video()
            self.enableFocusVideoTable()

    def previous(self):
        if self.playing_video:
            ids = []
            for id in self.tvVideos.get_children():
                ids.append(id)
            currentIndex = ids.index(self.videoIdColumnActive)
            index = currentIndex - 1
            nextMedia = None
            if currentIndex == 0:
                nextMedia = ids[len(ids) - 1]
            else:
                nextMedia = ids[index]
            self.stop_video()
            self.disableFocusVideoTable()
            self.videoIdColumnActive = nextMedia
            item = self.tvVideos.item(nextMedia)
            values = item['values']
            nombreVideo = values[0]
            playlistVideo = values[2]
            data = self.videosService.findVideoByName(nombreVideo, playlistVideo)
            self.current_file = data['fullpath']
            self.play_video()
            self.enableFocusVideoTable()

    def play_video(self):
        if self.current_file is not None:
            if not self.playing_video:

                self.tiempoActualLabel.config(text = "00:00:00")
                self.tiempoTotalLabel.config(text = self.get_duration_string())

                media = self.instance.media_new(self.current_file)

                self.media_player.set_media(media)

                self.tvVideos.place_forget()

                self.mostrarCanvaVideo()

                self.media_player.set_hwnd(self.media_canvas.winfo_id())

                self.media_player.play()

                self.playing_video = True

                self.reproducirCancion_btn.config(image = 'pause')

                self.controlar_estado_video()

            else:
                if self.video_paused:
                    self.media_player.play()
                    self.video_paused = False
                    self.reproducirCancion_btn.config(image = 'pause')
                else:
                    self.media_player.pause()
                    self.video_paused = True
                    self.reproducirCancion_btn.config(image = 'play')

    def stop_video(self, isRepeat = False):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False
            self.tiempoTotalLabel.config(text="00:00:00")
            self.tiempoActualLabel.config(text="00:00:00")
            self.barraProgreso.set(0)

            self.media_canvas.place_forget()
            self.mostrarTablaVideos()
            if self.repeatVideoMode == False:
                self.videoIdColumnActive = None
            self.cargarTabla()

    def format_time(self, value):
        seconds, milliseconds = divmod(value, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return ("%02i:%02i:%02i" % (hours, minutes, seconds))

    def controlar_estado_video(self):
        
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

            if self.media_player.get_state() in [vlc.State.Ended]:
                if self.repeatVideoMode == False:
                    self.next()
                else:
                    self.stop_video(True)
                    self.play_video()

        self.selfDash.after(1000, self.controlar_estado_video)

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
        if self.repeatVideoMode == False:
            self.modoRepetir_btn.config(image = 'repeat')
            self.repeatVideoMode = True
        else:
            self.modoRepetir_btn.config(image = 'norepeat')
            self.repeatVideoMode = False

    def loadPlaylistsVideos(self):
        print("playlists videos")
        self.videosPlaylists = formPlaylists()
        self.videosPlaylists.setDashboard(self)
        self.videosPlaylists.setMediaType(2)

    def enableFocusVideoTable(self):
        if self.videoIdColumnActive is not None:
            self.tvVideos.item(self.videoIdColumnActive, tags=['selected'])
        
    def disableFocusVideoTable(self):
        if self.videoIdColumnActive is not None:
            self.tvVideos.item(self.videoIdColumnActive, tags=['unselected'])

    def handleClickLoadVideo(self, event):

        self.stop_video()

        self.disableFocusVideoTable()

        itemFocus = self.tvVideos.focus()

        item = self.tvVideos.item(itemFocus)

        itemValues = item['values']

        nombreVideo = itemValues[0]
        playlistVideo = itemValues[2]
        
        data = self.videosService.findVideoByName(nombreVideo, playlistVideo)

        self.current_file = data['fullpath']
        self.play_video()

        self.tvVideos.selection_remove(self.tvVideos.selection())

        self.videoIdColumnActive = self.tvVideos.identify_row(event.y)
        self.videoIdActive = data["id"]

        self.enableFocusVideoTable()

    def mostrarTablaVideos(self):

        self.tvVideos = ttk.Treeview(
            self.selfDash,
            bootstyle='dark',
            show='headings',
            height=13,
            style='Videos.Treeview',
        )
        
        self.tvVideos.configure(columns=(
            'Título', 'Duración', 'Playlist'
        ))

        self.tvVideos.column('Título', width=524, stretch=True, anchor='center')
        self.tvVideos.column('Duración', width=150, stretch=True, anchor='center')
        self.tvVideos.column('Playlist', width=500, stretch=True, anchor='center')
                
        for col in self.tvVideos['columns']:
            self.tvVideos.heading(col, text=col.title(), anchor='center')

        self.tvVideos.place(x = 10, y = 70)

        scrollVideos = ttk.Scrollbar(self.selfDash, orient="vertical", bootstyle='secondary', command=self.tvVideos.yview)
        scrollVideos.place(x = 1200, y = 73, height = 550)

        self.tvVideos.configure(yscrollcommand=scrollVideos.set)

        self.tvVideos.tag_configure('selected', background='#526170')
        self.tvVideos.tag_configure('unselected', background='#32465A')

        self.tvVideos.bind("<Double-Button-1>", self.handleClickLoadVideo)
        self.tvVideos.unbind("<Button-1>")

        for video in self.videosList:
            title = video["title"]
            duration = video["duration"]
            playlist = video["playlist"]
            self.tvVideos.insert("","end",values=(title, duration, playlist), tags='unselected')

    def mostrarCanvaVideo(self):
        self.media_canvas = tk.Canvas(self.selfDash, bg="black", width=1180, height=570)
        self.media_canvas.place(x = 10, y = 70)

    def cargarTabla(self):
        for playlist_id in self.playlistsVideosSaved:
            videosList = self.videosService.getVideosByIdPlaylist(playlist_id)
            for video in videosList:
                title = video["title"]
                duration = video["duration"]
                playlist = video["playlist_name"]
                self.tvVideos.insert("","end",values=(title, duration, playlist), tags='unselected')

    def cargarMenuVideos(self, selfDash):

        self.selfDash = selfDash

        self.ventanaActiva = 2

        valorProgreso = 0
        valorVolumen = 100

        selfDash.ventana.destroy()

        selfDash.ventana = ttk.Frame(selfDash, bootstyle='secondary')
        selfDash.ventana.pack_propagate(0)
        selfDash.ventana.pack(side='left', fill='both', expand=True)

        self.mostrarTablaVideos()

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

        cargarCancionAtras_btn = ttk.Button(
            master=selfDash,
            image='previous',
            command=self.previous,
            style='ButtonIcon.TButton'
        )
        cargarCancionAtras_btn.place(x = 200, y = 760)

        self.reproducirCancion_btn = ttk.Button(
            master=selfDash,
            image='play', 
            command=self.play_video,
            style='ButtonIcon.TButton'
        )
        self.reproducirCancion_btn.place(x = 300, y = 760)

        cargarCancionAdelante_btn = ttk.Button(
            master=selfDash,
            image='next',
            command=self.next,
            style='ButtonIcon.TButton'
        )
        cargarCancionAdelante_btn.place(x = 400, y = 760)

        detenerCancion_btn = ttk.Button(
            master=selfDash,
            image='stop',
            command=self.stop_video,
            style='ButtonIcon.TButton'
        )
        detenerCancion_btn.place(x = 500, y = 760)      

        self.modoRepetir_btn = ttk.Button(
            master=selfDash,
            image='norepeat',
            style='ButtonIcon2.TButton',
            command=self.repeatMode,
        )
        self.modoRepetir_btn.place(x = 600, y = 760)

        cargarPlaylist_btn = ttk.Button(
            master=selfDash,
            image='playlist',
            command=self.loadPlaylistsVideos,
            style='ButtonIcon2.TButton',
        )
        cargarPlaylist_btn.place(x = 690, y = 760)

        self.barraVolumen = ttk.Scale(
            master=selfDash, 
            bootstyle="info",
            from_=0,
            to=100,
            length=250,
            value=valorVolumen,
            style='Custom.Horizontal.TScale'
        )
        self.barraVolumen.place(x = 860, y = 785)

        self.barraVolumen.bind("<Button-1>", self.handleVolumenSlider)
        self.barraVolumen.bind("<ButtonRelease>", self.handleVolumenSlider)

        self.cargarTabla()