#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import func
from database import get_session
from models import Video, PlaylistVideo

class VideosService:

    def getVideosByPlaylist(self, playlist):
        with get_session() as session:
            playlist_id = session.query(PlaylistVideo.id).filter(PlaylistVideo.name == playlist).first()
            if playlist_id:
                videos = (
                    session.query(
                        Video.id,
                        Video.title,
                        Video.duration_string,
                        Video.fullpath,
                        Video.playlist_id,
                    )
                    .filter(Video.playlist_id == playlist_id[0])
                    .order_by(Video.updated_at.desc())
                    .all()
                )
                return [playlist_id[0], [{
                    "id": video.id,
                    "title": video.title,
                    "duration": video.duration_string,
                    "fullpath": video.fullpath,
                    "playlist_id": video.playlist_id,
                    "playlist_name": playlist
                } for video in videos]]

        return [None, []]

    def getVideosByIdPlaylist(self, playlist_id):
        with get_session() as session:
            playlist = session.query(PlaylistVideo).filter(PlaylistVideo.id == playlist_id).first()
            if playlist:
                videos = (
                    session.query(
                        Video.id,
                        Video.title,
                        Video.duration_string,
                        Video.fullpath,
                        Video.playlist_id,
                    )
                    .filter(Video.playlist_id == playlist_id)
                    .order_by(Video.updated_at.desc())
                    .all()
                )
                return [{
                    "id": video.id,
                    "title": video.title,
                    "duration": video.duration_string,
                    "fullpath": video.fullpath,
                    "playlist_id": video.playlist_id,
                    "playlist_name": playlist.name
                } for video in videos]
            
        return []

    def findVideoByName(self, videoName, playlistName):
        with get_session() as session:
            playlist = session.query(PlaylistVideo).filter(PlaylistVideo.name == playlistName).first()
            if playlist:
                video = session.query(Video).filter(
                    Video.title == videoName, 
                    Video.playlist_id == playlist.id
                ).first()
                if video:
                    return {
                        "id": video.id,
                        "title": video.title,
                        "duration": video.duration_string,
                        "fullpath": video.fullpath,
                        "playlist_id": playlist.id
                    }
        return None
