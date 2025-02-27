from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from datetime import datetime
from database import Base

class PlaylistSong(Base):
    __tablename__ = 'playlist_song'
    id = Column(Integer(), primary_key=True)
    name = Column(String(150),unique=True)
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at =Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer(), primary_key=True)
    title = Column(String(150))
    duration_string = Column(Text())
    fullpath = Column(Text())
    playlist_id = Column(Integer(), ForeignKey('playlist_song.id'))
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class PlaylistVideo(Base):
    __tablename__ = 'playlist_video'
    id = Column(Integer(), primary_key=True)
    name = Column(String(150),unique=True)
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer(), primary_key=True)
    title = Column(String(150))
    duration_string = Column(Text())
    fullpath = Column(Text())
    playlist_id = Column(Integer(), ForeignKey('playlist_video.id'))
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class Stations(Base):
    __tablename__ = 'stations'
    id = Column(Integer(), primary_key=True)
    name = Column(String(150),unique=True)
    link = Column(String(200),unique=True)
    categories = Column(String(150))
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer(), primary_key=True)
    songs_directory = Column(String(200),unique=True)
    videos_directory = Column(String(200),unique=True)
    songs_directory_gd = Column(String(200),unique=True)
    songs_directory_downloads = Column(String(200),unique=True)
    videos_directory_downloads = Column(String(200),unique=True)
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)

class PlaylistHistory(Base):
    __tablename__ = 'playlist_history'
    id = Column(Integer(), primary_key=True)
    songs_list = Column(Text())
    videos_list = Column(Text())
    created_at = Column(DateTime(timezone=True), default = datetime.now)
    updated_at = Column(DateTime(timezone=True), default = datetime.now, onupdate = datetime.now)