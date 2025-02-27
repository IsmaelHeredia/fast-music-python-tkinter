#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import get_session
from models import PlaylistHistory

class HistoryService:

    def getPlaylistsSongsSaved(self):
        with get_session() as session:
            playlistsHistory = session.query(PlaylistHistory).first()
            playlists = []
            if playlistsHistory and playlistsHistory.songs_list:
                playlists = [int(playlist_id) for playlist_id in playlistsHistory.songs_list.split(",")]
            return playlists

    def setPlaylistsSongsSaved(self, playlists):
        playlistsList = ",".join(map(str, playlists))
        with get_session() as session:
            playlistsHistory = session.query(PlaylistHistory).first()
            if playlistsHistory:
                playlistsHistory.songs_list = playlistsList
                session.commit()

    def getPlaylistsVideosSaved(self):
        with get_session() as session:
            playlistsHistory = session.query(PlaylistHistory).first()
            playlists = []
            if playlistsHistory and playlistsHistory.videos_list:
                playlists = [int(playlist_id) for playlist_id in playlistsHistory.videos_list.split(",")]
            return playlists

    def setPlaylistsVideosSaved(self, playlists):
        playlistsList = ",".join(map(str, playlists))
        with get_session() as session:
            playlistsHistory = session.query(PlaylistHistory).first()
            if playlistsHistory:
                playlistsHistory.videos_list = playlistsList
                session.commit()
