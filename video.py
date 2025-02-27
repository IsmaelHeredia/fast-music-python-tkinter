#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Video Manager 1.0
# Written by Ismael Heredia
# 08/10/2019 - Version 0.8
# 01/01/2022 - Fix module
# 01/05/2024 - Update & fix functions
# pip install BeautifulSoup4
# pip install yt-dlp
# pip install moviepy
# pip install pytube

import argparse
from modules import videoManager

def main():

    parser = argparse.ArgumentParser(add_help=False)   

    group = parser.add_argument_group("Video Manager")
    
    group.add_argument("-download-video", dest="func_download_video", help="Enter link to download in MP4")
    group.add_argument("-download-song", dest="func_download_song", help="Enter link to download and convert in MP3")
    group.add_argument("-download-videos", dest="func_download_videos", help="Enter file with links to download in MP4")
    group.add_argument("-download-songs", dest="func_download_songs", help="Enter file with links for download to finally convert in MP3")
    group.add_argument("-convert-to-mp3", dest="func_convert_to_mp3", help="Enter video to convert in MP3")
    group.add_argument("-findsong-and-download", dest="func_findsong_and_download", help="Enter name to find in google and download to finally convert in MP3")
    group.add_argument("-findsongs-and-download", dest="func_findsongs_and_download", help="Enter file with names to find in google and download to finally convert in MP3")
    group.add_argument("-read-playlist", dest="func_read_playlist", help="Enter playlist to read links")
    group.add_argument("-download-playlist-videos", dest="func_download_playlist_videos", help="Enter playlist to download in MP4")
    group.add_argument("-download-playlist-songs", dest="func_download_playlist_songs", help="Enter playlist to download and convert in MP3")
    group.add_argument("-output-name", dest="func_output_name", help="Set the name with which the download will be saved, the name must be without extension")
    group.add_argument("-output-folder", dest="func_output_folder", help="Set the folder with which the download will be saved")

    group.add_argument("-set-music-folder", dest="func_set_music_folder", help="Enter optional directory to save songs")
    group.add_argument("-set-video-folder", dest="func_set_video_folder", help="Enter optional directory to save videos")

    results = parser.parse_args()

    func_download_video = results.func_download_video
    func_download_song = results.func_download_song
    
    func_download_videos = results.func_download_videos
    func_download_songs = results.func_download_songs

    func_convert_to_mp3 = results.func_convert_to_mp3

    func_findsong_and_download = results.func_findsong_and_download
    func_findsongs_and_download = results.func_findsongs_and_download

    func_read_playlist = results.func_read_playlist

    func_download_playlist_videos = results.func_download_playlist_videos
    func_download_playlist_songs = results.func_download_playlist_songs

    func_output_name = results.func_output_name
    func_output_folder = results.func_output_folder

    func_set_music_folder = results.func_set_music_folder
    func_set_video_folder = results.func_set_video_folder

    vm = videoManager.videoManager()

    if func_set_music_folder != None:
        vm.setMusicFolder(func_set_music_folder)

    if func_set_video_folder != None:
        vm.setVideoFolder(func_set_video_folder)

    if func_output_folder != None:
        vm.setOutputFolder(func_output_folder)

    if func_download_video != None:
        if func_output_name != None:
            vm.setNameVideo(func_output_name)
        vm.download_video(func_download_video,True)

    elif func_download_song != None:
        if func_output_name != None:
            vm.setNameSong(func_output_name) 
        filename = vm.download_video(func_download_song,False)
        vm.convert_to_mp3(vm.TEMP_VIDEO,filename)

    elif func_download_videos != None:
        vm.download_videos(func_download_videos,True)

    elif func_download_songs != None:
        vm.download_songs(func_download_songs)

    elif func_findsong_and_download != None:
        vm.findsong_and_download(func_findsong_and_download)

    elif func_findsongs_and_download != None:
        vm.findsongs_and_download(func_findsongs_and_download)

    elif func_download_playlist_videos != None:
        vm.download_playlist_videos(func_download_playlist_videos)

    elif func_download_playlist_songs != None:
        vm.download_playlist_songs(func_download_playlist_songs)

    elif func_convert_to_mp3 != None and func_output_name != None:
        vm.setNameSong(func_output_name)
        vm.convert_to_mp3(func_convert_to_mp3)

    elif func_read_playlist != None and func_output_name != None:
        vm.read_playlist(func_read_playlist,func_output_name)

    else:
        parser.print_help()

    vm.clear_temp()

if __name__ == "__main__":
    main()