#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from database import get_session
from functions import convert_to_duration
from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip

from models import Song, PlaylistSong, Video, PlaylistVideo, Configuration

load_dotenv()

class ConfigurationService:
    
    def cargarConfiguracion(self):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config:
                return None
            
            return {
                "songs_directory": config.songs_directory or "",
                "videos_directory": config.videos_directory or "",
                "songs_directory_gd": config.songs_directory_gd or "",
                "songs_directory_downloads": config.songs_directory_downloads or "",
                "videos_directory_downloads": config.videos_directory_downloads or "",
            }

    def fijarDirectoriosMultimedia(self, directorio_canciones, directorio_videos):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config:
                config = Configuration()
                session.add(config)

            config.songs_directory = directorio_canciones
            config.videos_directory = directorio_videos
            session.commit()

    def fijarDirectorioGD(self, directorio_canciones_gd):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config:
                config = Configuration()
                session.add(config)

            config.songs_directory_gd = directorio_canciones_gd
            session.commit()

    def fijarDirectoriosDescargas(self, directorio_canciones, directorio_videos):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config:
                config = Configuration()
                session.add(config)

            config.songs_directory_downloads = directorio_canciones
            config.videos_directory_downloads = directorio_videos
            session.commit()

    def scanSongs(self):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config or not config.songs_directory:
                return False

            sync_folder = config.songs_directory
            existing_playlists = {p.name: p.id for p in session.query(PlaylistSong).all()}
            existing_songs = {s.fullpath for s in session.query(Song).all()}

            new_songs = []
            new_playlists = {}

            for root, _, files in os.walk(sync_folder):
                playlist_name = os.path.basename(root)
                playlist_id = existing_playlists.get(playlist_name)

                if not playlist_id:
                    new_playlist = PlaylistSong(name=playlist_name)
                    session.add(new_playlist)
                    session.flush()
                    playlist_id = new_playlist.id
                    new_playlists[playlist_name] = playlist_id

                files = sorted(files, key=lambda f: os.path.getctime(os.path.join(root, f)), reverse=True)

                for file in files:
                    if file.endswith(".mp3"):
                        path = os.path.join(root, file)
                        if path not in existing_songs:
                            audio = MP3(path)
                            new_songs.append(Song(
                                title=os.path.splitext(file)[0],
                                duration_string=convert_to_duration(audio.info.length),
                                fullpath=path,
                                playlist_id=playlist_id
                            ))

            if new_songs:
                session.bulk_save_objects(new_songs)
                session.commit()
            return True

    def scanVideos(self):
        with get_session() as session:
            config = session.query(Configuration).first()
            if not config or not config.videos_directory:
                return False

            sync_folder = config.videos_directory
            existing_playlists = {p.name: p.id for p in session.query(PlaylistVideo).all()}
            existing_videos = {v.fullpath for v in session.query(Video).all()}

            new_videos = []
            new_playlists = {}

            for root, _, files in os.walk(sync_folder):
                playlist_name = os.path.basename(root)
                playlist_id = existing_playlists.get(playlist_name)

                if not playlist_id:
                    new_playlist = PlaylistVideo(name=playlist_name)
                    session.add(new_playlist)
                    session.flush()
                    playlist_id = new_playlist.id
                    new_playlists[playlist_name] = playlist_id

                files = sorted(files, key=lambda f: os.path.getctime(os.path.join(root, f)), reverse=True)

                def process_video(file):
                    path = os.path.join(root, file)
                    if path not in existing_videos:
                        video = VideoFileClip(path)
                        return Video(
                            title=os.path.splitext(file)[0],
                            duration_string=convert_to_duration(video.duration),
                            fullpath=path,
                            playlist_id=playlist_id
                        )

                with ThreadPoolExecutor(max_workers=4) as executor:
                    results = list(executor.map(process_video, [f for f in files if f.endswith(".mp4")]))
                    new_videos.extend(filter(None, results))

            if new_videos:
                session.bulk_save_objects(new_videos)
                session.commit()
            return True
