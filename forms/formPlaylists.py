#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import ttkbootstrap as ttk

from services.songsService import SongsService
from services.videosService import VideosService
from services.playlistsService import PlaylistsService
from services.historyService import HistoryService

from pathlib import Path

class formPlaylists(ttk.Toplevel):

    style = {"background": '#4e5d6c'}

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.playlistsService = PlaylistsService()
        self.songsService = SongsService()
        self.videosService = VideosService()
        self.historyService = HistoryService()
        
        self.playlistsSongsSaved = self.historyService.getPlaylistsSongsSaved()
        self.playlistsVideosSaved = self.historyService.getPlaylistsVideosSaved()

        self.playlists_id = []

        self.mediaType = None

        iconosLista = {
            'select': 'plus.png',
            'trash': 'trash.png',
        }

        self.iconos = []

        imgpath = Path(__file__).parent / '../icons'
        for key, val in iconosLista.items():
            _path = imgpath / val
            self.iconos.append(ttk.PhotoImage(name=key, file=_path))

        self.geometry('800x780')
        self.title('Seleccionar playlists')
        self.position_center()
        self.resizable(False, False)

        self.ventana = ttk.Frame(self, bootstyle='secondary')
        self.ventana.pack_propagate(0)
        self.ventana.pack(side='left', fill='both', expand=True)

        self.buscarLabel = ttk.Label(self, text="Nombre", **self.style)
        self.buscarLabel.place(x = 30, y = 23)

        self.buscarEntry = ttk.Entry(self, width=74)
        self.buscarEntry.place(x = 120, y = 23)

        self.buscarButton = ttk.Button(self, text="Buscar", command=self.buscarCanciones)
        self.buscarButton.place(x = 600, y = 23)

        self.tvPlaylists = ttk.Treeview(
            self.ventana,
            bootstyle='dark',
            show='headings',
            height=13,
            style='Playlist.Treeview',
        )
        
        self.tvPlaylists.configure(columns=('Titulo','Cantidad'))

        self.tvPlaylists.column('Titulo', width=524, stretch=True, anchor='center')
        self.tvPlaylists.column('Cantidad', width=150, stretch=True, anchor='center')
                
        self.tvPlaylists.heading('#1', text='Titulo', anchor='center')
        self.tvPlaylists.heading('#2', text='Cantidad', anchor='center')

        self.tvPlaylists.tag_configure('checked', background='#6294AB')
        self.tvPlaylists.tag_configure('unchecked', background='#343A40')

        self.tvPlaylists.place(x = 10, y = 110)

        scrollPlaylists = ttk.Scrollbar(self.ventana, orient="vertical", bootstyle='secondary', command=self.tvPlaylists.yview)
        scrollPlaylists.place(x = 690, y = 110, height = 550)
        self.tvPlaylists.configure(yscrollcommand=scrollPlaylists.set)

        self.seleccionarButton = ttk.Button(self, text="Seleccionar", command=self.handleClickSeleccionar)
        self.seleccionarButton.place(x = 230, y = 700)

        self.cancelarButton = ttk.Button(self, text="Cancelar", command=self.handleClickCancelar)
        self.cancelarButton.place(x = 380, y = 700)

        self.seleccionarTodo = ttk.Button(
            master=self.ventana,
            image='select',
            style='ButtonIcon.TButton',
            command=self.handleClickSeleccionarTodo
        )
        self.seleccionarTodo.place(x = 720, y = 300)

        self.cancelarTodo = ttk.Button(
            master=self.ventana,
            image='trash',
            style='ButtonIcon.TButton',
            command=self.handleClickCancelarTodo
        )
        self.cancelarTodo.place(x = 720, y = 360)    

        self.tvPlaylists.bind('<ButtonRelease-1>', self.handleClickPlaylist)
        self.tvPlaylists.unbind("<Button-1>")

    def setDashboard(self, master):
        self.dashboard = master

    def setMediaType(self, mediaType):
        self.mediaType = mediaType
        if mediaType == 1:
            self.playlists_id = self.playlistsSongsSaved
        elif mediaType == 2:
            self.playlists_id = self.playlistsVideosSaved
        self.buscarCanciones()

    def handleClickPlaylist(self, event):

        itemFocus = self.tvPlaylists.focus()

        item = self.tvPlaylists.item(itemFocus)

        tags = item['tags']

        if len(tags) > 0:

            currentTag = tags[0]

            _iid = self.tvPlaylists.identify_row(event.y)

            nombrePlaylist = self.tvPlaylists.item(_iid)['values'][0]

            playlist = []

            if self.mediaType == 1:
                playlist = self.playlistsService.getPlaylistSongByName(nombrePlaylist)
            elif self.mediaType == 2:
                playlist = self.playlistsService.getPlaylistVideoByName(nombrePlaylist)

            playlistId = playlist['id']

            if currentTag == 'checked':
                self.tvPlaylists.item(_iid, tags=['unchecked'])
                self.playlists_id.remove(playlistId)
            else:
                self.tvPlaylists.item(_iid, tags=['checked'])
                self.playlists_id.append(playlistId)

        self.tvPlaylists.selection_remove(self.tvPlaylists.selection())

    def handleClickSeleccionar(self):

        if self.mediaType == 1:
            self.dashboard.songIdColumnActive = None
            for i in self.dashboard.tvCanciones.get_children():
                self.dashboard.tvCanciones.delete(i)
        elif self.mediaType == 2:
            self.dashboard.videoIdColumnActive = None
            for i in self.dashboard.tvVideos.get_children():
                self.dashboard.tvVideos.delete(i)

        playlistSongsSaved = []
        playlistVideosSaved = []

        for line in self.tvPlaylists.get_children():
            _iid = line
            item = self.tvPlaylists.item(_iid)
            playlist = item["values"][0]

            mediaList = []

            if self.mediaType == 1:
                playlist_selected_id, mediaList = self.songsService.getSongsByPlaylist(playlist)
            elif self.mediaType == 2:
                playlist_selected_id, mediaList = self.videosService.getVideosByPlaylist(playlist)

            videosList = []

            if playlist_selected_id in self.playlists_id:

                for media in mediaList:
                    idMedia = media["id"]
                    title = media["title"]
                    duration = media["duration"]
                    fullpath = media["fullpath"]
                    playlist_id = media["playlist_id"]
                    if self.mediaType == 1:
                        self.dashboard.tvCanciones.insert("","end",values=(title, duration, playlist), tags='unselected')
                        if playlist_id not in playlistSongsSaved:
                            playlistSongsSaved.append(playlist_id)
                    elif self.mediaType == 2:
                        self.dashboard.tvVideos.insert("","end",values=(title, duration, playlist), tags='unselected')
                        videosList.append({
                            "id": idMedia,
                            "title": title,
                            "duration": duration,
                            "fullpath": fullpath,
                            "playlist": playlist
                        })
                        if playlist_id not in playlistVideosSaved:
                            playlistVideosSaved.append(playlist_id)
                    
                if self.mediaType == 2:
                    self.dashboard.videosList = videosList

        if self.mediaType == 1:
            self.historyService.setPlaylistsSongsSaved(playlistSongsSaved)
        elif self.mediaType == 2:
            self.historyService.setPlaylistsVideosSaved(playlistVideosSaved)
            self.dashboard.videosList = videosList

        self.destroy()

    def handleClickCancelar(self):
        self.destroy()

    def handleClickSeleccionarTodo(self):
        self.playlists_id = []

        playlistsLista = []

        if self.mediaType == 1:
            playlistsLista = self.playlistsService.getPlaylistsSongs("")
        elif self.mediaType == 2:
            playlistsLista = self.playlistsService.getPlaylistsVideos("")

        for playlist in playlistsLista:
            self.playlists_id.append(playlist["id"])

        for _iid in self.tvPlaylists.get_children():
            self.tvPlaylists.item(_iid, tags=['checked'])

    def handleClickCancelarTodo(self):
        self.playlists_id = []

        for _iid in self.tvPlaylists.get_children():
            self.tvPlaylists.item(_iid, tags=['unchecked'])

    def buscarCanciones(self):

        for i in self.tvPlaylists.get_children():
            self.tvPlaylists.delete(i)

        playlistsLista = []

        if self.mediaType == 1:
            playlistsLista = self.playlistsService.getPlaylistsSongs(self.buscarEntry.get())
        elif self.mediaType == 2:
            playlistsLista = self.playlistsService.getPlaylistsVideos(self.buscarEntry.get())

        for playlist in playlistsLista:
            tag = ""
            
            if int(playlist["id"]) in self.playlists_id:
                tag = "checked"
            else:
                tag = "unchecked"

            self.tvPlaylists.insert("","end",values=(playlist["name"],playlist["count"]), tags=tag)