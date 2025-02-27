#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Ismael Heredia
# pip install yt-dlp
# pip install --upgrade yt-dlp
# pip install yt-dlp --upgrade
# 01/01/2022 - Module youtube_dl was changed for yt_dlp

from modules import colors
from modules import googleSearch
import os,re,time
from yt_dlp import YoutubeDL
from pytube import Playlist
import moviepy.editor as mp

class videoManager(object):

    def __init__(self):

        self.gs = googleSearch.googleSearch()
        
        self.music_folder = ""
        self.videos_folder = ""
        
        if os.name == "nt":
            self.music_folder = "Music"
            self.videos_folder = "Videos"
        else:
            self.music_folder = "Música"
            self.videos_folder = "Vídeos"
            
        self.directory = os.path.join(os.path.expanduser("~"), self.music_folder) + "/Video_downloads"
        self.directory_videos = os.path.join(os.path.expanduser("~"), self.videos_folder) + "/Video_downloads"

        self.TEMP_VIDEO = self.directory + "/temp_video.mp4"

        self.name_video = None
        self.name_song = None
        self.output_folder = None

        self.timeout_wait = 5

        self.ydl_opts_videos = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]',
            "outtmpl": self.TEMP_VIDEO,
            "ignoreerrors": True,
            "cachedir": False
        }

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.exists(self.directory_videos):
            os.makedirs(self.directory_videos)

        self.clear_temp()

    def setNameVideo(self,name_video):
        self.name_video = name_video

    def setNameSong(self,name_song):
        self.name_song = name_song

    def setOutputFolder(self,output_folder):
        self.output_folder = output_folder

    def setMusicFolder(self,music_folder):
        self.directory = music_folder
        self.TEMP_VIDEO = self.directory + "/temp_video.mp4"

    def setVideoFolder(self,video_folder):
        self.directory_videos = video_folder

    def clear_temp(self):
        temp_songs = self.directory  + "/temp_video.mp4"
        temp_videos = self.directory_videos + "/temp_video.mp4"

        if os.path.isfile(temp_songs):
            os.remove(temp_songs)
        if os.path.isfile(temp_videos):
            os.remove(temp_videos)

    def download_video(self,video,only_video=False):

        video = video.replace("\n", "")

        if os.path.isfile(self.TEMP_VIDEO):
            os.remove(self.TEMP_VIDEO)

        print(colors.config.INFO + "\n[+] Downloading video {} ...\n" . format(video) + colors.config.ENDC)
        
        try:
            with YoutubeDL(self.ydl_opts_videos) as ydl:
                info_dict = ydl.extract_info(video, download=False)

                video_title = ""

                if self.name_video is None:
                    video_title = info_dict.get("title", None)
                    video_title = re.sub(r'[\\/*?:"<>|]',"",video_title)
                else:
                    video_title = self.name_video

                print(colors.config.INFO2 + "\n[+] Title : {}\n" . format(video_title) + colors.config.ENDC)

                ydl.download([video])

                if only_video:

                    video_path = ""

                    if self.output_folder is None:
                        video_path = self.directory_videos + "/" + video_title + ".mp4"
                    else:
                        check_folder = self.directory_videos + "/" + self.output_folder
                        if not os.path.exists(check_folder):
                            os.makedirs(check_folder)
                        video_path = check_folder + "/" + video_title + ".mp4"

                    if not os.path.isfile(video_path):
                        os.rename(self.TEMP_VIDEO,video_path)

                    print(colors.config.OK + "\n[!] Saved in {}" . format(video_path) + colors.config.ENDC)

                return video_title
                
        except:
            print(colors.config.FAIL + "\n[-] Error downloading video" + colors.config.ENDC)
            #raise

    def convert_to_mp3(self,video,name=""):

        video = video.replace("\n", "")

        if os.path.isfile(video):

            print(colors.config.INFO + "\n[+] Converting video {} to mp3 ...\n" . format(video) + colors.config.ENDC)

            filename = name

            pre = ""

            if self.name_song is None:
                pre, ext = os.path.splitext(os.path.basename(filename))
            else:
                pre = self.name_song

            filename = pre + ".mp3"

            fullpath = ""

            if self.output_folder is None:
                fullpath = self.directory + "/" + filename
            else:
                check_folder = self.directory + "/" + self.output_folder
                if not os.path.exists(check_folder):
                    os.makedirs(check_folder)
                fullpath = check_folder + "/" + filename

            try:
                clip = mp.VideoFileClip(video)
                clip = clip.subclip(0,clip.duration)
                clip.audio.write_audiofile(fullpath)
                self.close_clip(clip)
                print(colors.config.OK + "\n[!] Saved in {}" . format(fullpath) + colors.config.ENDC)
                return fullpath
            except:
                print(colors.config.FAIL + "\n[-] Error converting mp3" + colors.config.ENDC)
                #raise

        else:
            print(colors.config.RED + "\n[-] File not found" + colors.config.ENDC)

    def download_videos(self,filename,only_video=False):
        print(colors.config.INFO + "\n[+] Opening file {} ..." . format(filename) + colors.config.ENDC)
        if os.path.exists(filename): 
            with open(filename) as f:
                lines = f.readlines()
                total = len(lines)
                counter = 0
                for link in lines:
                    counter += 1
                    print(colors.config.STATUS + "\n[+] Status {}/{} ..." . format(counter,total) + colors.config.ENDC)
                    self.download_video(link,only_video)
                    time.sleep(self.timeout_wait)
        else:
            print(colors.config.FAIL + "\n[-] File not found" + colors.config.ENDC)

    def download_songs(self,filename):
        print(colors.config.INFO + "\n[+] Opening file {} ..." . format(filename) + colors.config.ENDC)
        if os.path.exists(filename): 
            with open(filename) as f:
                lines = f.readlines()
                total = len(lines)
                counter = 0
                for link in lines:
                    counter += 1
                    print(colors.config.STATUS + "\n[+] Status {}/{} ..." . format(counter,total) + colors.config.ENDC)
                    filename = self.download_video(link,False)
                    self.convert_to_mp3(self.TEMP_VIDEO,filename)
                    time.sleep(self.timeout_wait)
        else:
            print(colors.config.RED + "\n[-] File not found" + colors.config.ENDC)

    def findsong_and_download(self,name):
        name = name.strip("\n")
        print(colors.config.INFO + "\n[+] Searching song {} ..." . format(name) + colors.config.ENDC)
        string = "site:https://www.youtube.com " + name
        link = self.gs.send_first_result(string)
        if link:
            filename = self.download_video(link,False)
            mp3_file = self.convert_to_mp3(self.TEMP_VIDEO,filename)
            return mp3_file
        else:
            print(colors.config.FAIL + "\n[-] Song not found" + colors.config.ENDC)

    def findsongs_and_download(self,filename):
        print(colors.config.INFO + "\n[+] Opening file {} ..." . format(filename) + colors.config.ENDC)
        if os.path.exists(filename): 
            with open(filename) as f:
                lines = f.readlines()
                total = len(lines)
                counter = 0
                for name in lines:
                    counter += 1
                    print(colors.config.STATUS + "\n[+] Status {}/{} ..." . format(counter,total) + colors.config.ENDC)
                    self.findsong_and_download(name)
                    time.sleep(self.timeout_wait)
        else:
            print(colors.config.FAIL + "\n[-] File not found" + colors.config.ENDC)

    def read_playlist(self,playlist_link,filename):
        print(colors.config.INFO + "\n[+] Reading playlist {} ...\n" . format(playlist_link) + colors.config.ENDC)
        filename = filename + ".txt"
        try:
            links = Playlist(playlist_link)
            mode = ""
            if os.path.exists(filename):
                mode = "a"
            else:
                mode = "w"
            playlist_file = open(filename,mode, encoding="utf-8")
            for link in links:
                print(colors.config.OK + "[+] Link : {}" . format(link) + colors.config.ENDC)
                playlist_file.write(link + "\n")
            playlist_file.close()
        except:
            print(colors.config.FAIL + "\n[-] Error reading playlist" + colors.config.ENDC)
            #raise

    def download_playlist_videos(self,playlist_link):
        print(colors.config.INFO + "\n[+] Reading playlist {} ..." . format(playlist_link) + colors.config.ENDC)
        try:
            links = Playlist(playlist_link)
            total = len(links)
            counter = 0
            for link in links:
                counter += 1
                print(colors.config.STATUS + "\n[+] Status {}/{} ..." . format(counter,total) + colors.config.ENDC)
                self.download_video(link,True)
                time.sleep(self.timeout_wait)
        except:
            print(colors.config.FAIL + "\n[-] Error download playlist" + colors.config.ENDC)
            #raise

    def download_playlist_songs(self,playlist_link):
        print(colors.config.INFO + "\n[+] Reading playlist {} ..." . format(playlist_link) + colors.config.ENDC)
        try:
            links = Playlist(playlist_link)
            total = len(links)
            counter = 0
            for link in links:
                counter += 1
                print(colors.config.STATUS + "\n[+] Status {}/{} ..." . format(counter,total) + colors.config.ENDC)
                filename = self.download_video(link,False)
                savefile = os.path.basename(filename)
                self.convert_to_mp3(self.TEMP_VIDEO,savefile)
                time.sleep(self.timeout_wait)
        except:
            print(colors.config.FAIL + "\n[-] Error download playlist" + colors.config.ENDC)
            #raise

    def close_clip(self,video_clip):
        try:
            video_clip.reader.close()
            del video_clip.reader
            if video_clip.audio is not None:
                video_clip.audio.reader.close_proc()
                del video_clip.audio
            del video_clip
        except Exception:
            pass