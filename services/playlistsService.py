#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload
from sqlalchemy import func
from database import get_session
from models import PlaylistSong, Song, PlaylistVideo, Video

class PlaylistsService:
    
    def getPlaylistsSongs(self, name):
        with get_session() as session:
            playlists = (
                session.query(
                    PlaylistSong.id,
                    PlaylistSong.name,
                    func.count(Song.id).label("count")
                )
                .outerjoin(Song, PlaylistSong.id == Song.playlist_id)
                .filter(PlaylistSong.name.ilike(f"%{name}%"))
                .group_by(PlaylistSong.id, PlaylistSong.name)
                .order_by(PlaylistSong.name.asc())
                .all()
            )

            return [{"id": p.id, "name": p.name, "count": p.count} for p in playlists]

    def getPlaylistSongByName(self, name):
        with get_session() as session:
            playlist = session.query(PlaylistSong).filter(PlaylistSong.name == name).first()
            return {"id": playlist.id, "name": playlist.name} if playlist else None

    def getPlaylistsVideos(self, name):
        with get_session() as session:
            playlists = (
                session.query(
                    PlaylistVideo.id,
                    PlaylistVideo.name,
                    func.count(Video.id).label("count")
                )
                .outerjoin(Video, PlaylistVideo.id == Video.playlist_id)
                .filter(PlaylistVideo.name.ilike(f"%{name}%"))
                .group_by(PlaylistVideo.id, PlaylistVideo.name)
                .order_by(PlaylistVideo.name.asc())
                .all()
            )

            return [{"id": p.id, "name": p.name, "count": p.count} for p in playlists]

    def getPlaylistVideoByName(self, name):
        with get_session() as session:
            playlist = session.query(PlaylistVideo).filter(PlaylistVideo.name == name).first()
            return {"id": playlist.id, "name": playlist.name} if playlist else None
