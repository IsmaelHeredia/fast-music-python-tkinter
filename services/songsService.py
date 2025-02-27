#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import get_session
from models import Song, Video, PlaylistSong, PlaylistVideo

class SongsService:
    
    def getSongsByPlaylist(self, playlist):
        songsList = []
        with get_session() as session:
            playlist_entry = session.query(PlaylistSong).filter(PlaylistSong.name == playlist).first()
            if not playlist_entry:
                return None
            
            songs = session.query(Song).filter(Song.playlist_id == playlist_entry.id).order_by(Song.updated_at.desc()).all()
            for song in songs:
                songsList.append({
                    "id": song.id,
                    "title": song.title,
                    "duration": song.duration_string,
                    "fullpath": song.fullpath,
                    "playlist_id": playlist_entry.id,
                    "playlist_name": playlist
                })
        return [playlist_entry.id, songsList]
    
    def getSongsByIdPlaylist(self, playlist_id):
        songsList = []
        with get_session() as session:
            playlist_entry = session.query(PlaylistSong).filter(PlaylistSong.id == playlist_id).first()
            if not playlist_entry:
                return None
            
            songs = session.query(Song).filter(Song.playlist_id == playlist_id).order_by(Song.updated_at.desc()).all()
            for song in songs:
                songsList.append({
                    "id": song.id,
                    "title": song.title,
                    "duration": song.duration_string,
                    "fullpath": song.fullpath,
                    "playlist_id": playlist_id,
                    "playlist_name": playlist_entry.name
                })
        return songsList
    
    def findSongByName(self, songName, playlistName):
        with get_session() as session:
            playlist = session.query(PlaylistSong).filter(PlaylistSong.name == playlistName).first()
            if not playlist:
                return None
            
            song = session.query(Song).filter(Song.title == songName, Song.playlist_id == playlist.id).first()
            if song:
                return {
                    "id": song.id,
                    "title": song.title,
                    "duration": song.duration_string,
                    "fullpath": song.fullpath,
                    "playlist_id": playlist.id
                }
        return None

    def getVideosByPlaylist(self, playlist):
        videosList = []
        with get_session() as session:
            playlist_entry = session.query(PlaylistVideo).filter(PlaylistVideo.name == playlist).first()
            if not playlist_entry:
                return None
            
            videos = session.query(Video).filter(Video.playlist_id == playlist_entry.id).order_by(Video.updated_at.desc()).all()
            for video in videos:
                videosList.append({
                    "id": video.id,
                    "title": video.title,
                    "duration": video.duration_string,
                    "fullpath": video.fullpath,
                    "playlist_id": playlist_entry.id,
                    "playlist_name": playlist
                })
        return videosList
    
    def findVideoByName(self, videoName, playlistName):
        with get_session() as session:
            playlist = session.query(PlaylistVideo).filter(PlaylistVideo.name == playlistName).first()
            if not playlist:
                return None
            
            video = session.query(Video).filter(Video.title == videoName, Video.playlist_id == playlist.id).first()
            if video:
                return {
                    "id": video.id,
                    "title": video.title,
                    "duration": video.duration_string,
                    "fullpath": video.fullpath,
                    "playlist_id": playlist.id
                }
        return None
