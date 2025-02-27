#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs.dialogs import Messagebox

from services import configurationService

import threading

from ttkbootstrap.constants import *

from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth

import os, hashlib, shutil

class formSincronizacion(object):

    def __init__(self):

        self.style = {"background": '#4e5d6c'}
        
        self.selfDash = None

        self.drive = None

        self.tree_gd = []
        self.tree_folders_gd = []

        self.configurationService = configurationService.ConfigurationService()

        self.config = self.configurationService.cargarConfiguracion()

        self.folder_pc = self.config["songs_directory"]
        self.folder_gd_music = self.config["songs_directory_gd"]

        self.sincronizarGD_btn = None
        self.sincronizarPC_btn = None

    def insertarTabla(self, nombre, tipo, estado, id = None):
        idRow = None
        if id == None:
            idRow = self.tvArchivos.insert("","end",values=(nombre, tipo, estado,))
        else:
            self.tvArchivos.item(id, values=(nombre, tipo, estado),)
            idRow = id
        self.tvArchivos.yview_moveto(1)
        self.selfDash.update()
        return idRow
    
    def limpiar_tabla(self):
        for i in self.tvArchivos.get_children():
            self.tvArchivos.delete(i)

    def limpiar_consola(self):
        self.textConsole.text.configure(state="normal")
        self.textConsole.delete("1.0", END)
        self.textConsole.insert(END, "[+] Registros de sincronización habilitados\n\n")
        self.textConsole.text.configure(state="disabled")
    
    def escribir_consola(self, texto):
        self.textConsole.text.configure(state="normal")
        self.textConsole.insert(END, texto + "\n")
        self.textConsole.text.configure(state="disabled")
        self.textConsole.text.see("end")
        self.selfDash.update()
    
    def getIdByFolderName(self, name):
        for file_gd in self.tree_folders_gd:
            check_name = file_gd["name"]
            if name == check_name:
                return file_gd["id"]
        return None

    def filterLocalFilesFolder(self, folder):
        result = []
        folder_path = self.folder_pc + "/" + folder
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)    
            for file in files:
                fullpath = folder_path + "/" + file
                if os.path.isfile(fullpath):
                    result.append(file)
        return result

    def filterFolders(self):
        result = []
        for file_gd in self.tree_folders_gd:
            folder = file_gd["name"]
            if folder not in result:
                result.append(folder)
        return result

    def filterFilesFolder(self, folder):
        result = []
        for file_gd in self.tree_gd:
            if file_gd["folder"] == folder:
                result.append(file_gd)
        return result
                
    def get_folder_id_by_name(self, folder_name):
        files = self.drive.ListFile({"q": "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        if files != []:
            id_found = files[0]["id"]
            return id_found

    def getMD5File(self, filename):
        with open(filename, "rb") as file_to_check:
            data = file_to_check.read()    
            md5_returned = hashlib.md5(data).hexdigest()
            return md5_returned

    def downloadFile(self, id_drive, file, filename, md5):   
        idRow = None                
        try:             
            if os.path.isfile(filename):
                md5_file_pc = self.getMD5File(filename)
                idRow = self.insertarTabla(file, "Archivo", "Verificado")
            else:
                idRow = self.insertarTabla(file, "Archivo", "Descargando")
                self.escribir_consola("[+] Descargando archivo : %s - %s" % (id_drive,file))
                archivo = self.drive.CreateFile({"id": id_drive}) 
                archivo.GetContentFile(filename)
                self.escribir_consola("[+] Descargado")
                self.insertarTabla(file, "Archivo", "Descargado", idRow)
        except:
            self.escribir_consola("[-] Error descargando archivo")
            self.insertarTabla(file, "Archivo", "Error", idRow)
        
    def uploadFile(self, id_folder, fullpath):  
        idRow = None 
        self.escribir_consola("[+] Subiendo archivo : %s" % (fullpath,))
        filename = os.path.basename(fullpath)        
        try:  
            idRow = self.insertarTabla(filename, "Archivo", "Subiendo")
            new_file = self.drive.CreateFile({'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
            new_file['title'] = fullpath.split("/")[-1]
            new_file.SetContentFile(fullpath)
            
            new_file.Upload()
            
            self.insertarTabla(filename, "Archivo", "Subido", idRow)
            self.escribir_consola("[+] Archivo subido con ID %s" % (new_file["id"],))
            
            return new_file["id"]
        
        except:
            self.insertarTabla(filename, "Archivo", "Error", idRow)
            self.escribir_consola("[-] Error subiendo archivo")
            return None
        
    def makeFolderDrive(self, id_folder_gd, folder):
        idRow = None
        self.escribir_consola("[+] Creando carpeta %s" % (folder,))
        try:
            idRow = self.insertarTabla(folder, "Directorio", "Creando")

            new_folder = self.drive.CreateFile({
            'title': folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{"kind": "drive#fileLink", "id": id_folder_gd }]})
            
            new_folder.Upload()
                                        
            self.insertarTabla(folder, "Directorio", "Creado", idRow)
            self.escribir_consola("[+] Carpeta creada con ID %s" % (new_folder["id"],))
        
            return new_folder["id"]
        except:
            self.insertarTabla(folder, "Directorio", "Error", idRow)
            self.escribir_consola("[-] Error creando carpeta")
            return None

    def deleteFileGD(self,id_file,filename):
        idRow = None
        self.escribir_consola("[+] Borrando archivo : %s" % (filename,))
        try:
            idRow = self.insertarTabla(filename, "Archivo", "Borrando")

            delete_file = self.drive.CreateFile({"id": id_file})
            
            delete_file.Trash()
            delete_file.UnTrash()
            delete_file.Delete()
            
            self.insertarTabla(filename, "Archivo", "Borrado", idRow)
            self.escribir_consola("[+] Archivo borrado")

        except:
            self.insertarTabla(filename, "Archivo", "Error", idRow)
            self.escribir_consola("[-] Error borrando archivo")
            
    def deleteFolderGD(self,id_folder,folder_name):
        idRow = None
        self.escribir_consola("[+] Borrando carpeta : %s" % (folder_name,))

        try:
            idRow = self.insertarTabla(folder_name, "Directorio", "Borrando")

            delete_file = self.drive.CreateFile({"id": id_folder})
            
            delete_file.Trash()
            delete_file.UnTrash()
            delete_file.Delete()
            
            self.insertarTabla(folder_name, "Directorio", "Borrado", idRow)
            self.escribir_consola("[+] Carpeta borrada")

        except:
            self.insertarTabla(folder_name, "Directorio", "Error", idRow)
            self.escribir_consola("[-] Error borrando carpeta")

    def list_folder_gd(self, folder_id = None, folder_name = None):
        
        if folder_name != None:
            self.escribir_consola("[+] Leyendo directorio con nombre : %s" % folder_name)

        self.selfDash.update()
        
        query = ""
        
        if folder_id is None:
            query = "'root' in parents and trashed=false"
        else:
            query = "'" + str(folder_id) + "' in parents and trashed=false"
    
        try:
            file_list = self.drive.ListFile({"q": query, 'fields': 'items(id, title, mimeType, md5Checksum)' }).GetList()
            
            files = []
            folders = []
                
            for file in file_list:
                
                #print(file)
                id_drive = file["id"]
                title = file["title"]
                mimeType = file["mimeType"]
                md5 = ""
                
                if "md5Checksum" in file:
                    md5 = file['md5Checksum']
                if mimeType == "application/vnd.google-apps.folder":
                    folders.append({ "id" : id_drive, "name" : title })
                    if not any(d['name'] == title for d in self.tree_folders_gd):
                        self.tree_folders_gd.append({ "id" : id_drive, "name" : title })
                    #print("[+] Folder : %s" % (title,))
                else:
                    files.append({ "id" : id_drive, "name" : title })
                    self.tree_gd.append({ "id": id_drive, "folder": folder_name, "file": title, "md5": md5 })
                    #print("[+] File : %s" % (title,))
                    
            for folder in folders:
                self.selfDash.update()
                self.list_folder_gd(folder["id"],folder["name"])
                
        except:
            self.escribir_consola("[-] Error leyendo carpeta %s" % (folder["name"],))
            self.selfDash.update()

    def sync_from_drive(self):

        self.limpiar_tabla()
        self.limpiar_consola()
        
        id_folder_gd = self.get_folder_id_by_name(self.folder_gd_music)

        self.escribir_consola("[+] Leyendo carpetas y archivos de Google Drive ...\n")

        self.list_folder_gd(id_folder_gd)
        
        self.escribir_consola("\n[+] Limpiando carpetas")
        
        folders = []
        
        for folder_gd in self.tree_gd:
            folders.append(folder_gd["folder"])
            
        folders = list(set(folders))
                
        for list_name in os.listdir(self.folder_pc):
            list_path = os.path.join(self.folder_pc, list_name)
            folder_path = self.folder_pc + "/" + list_name
            if os.path.isdir(list_path):
                if list_name not in folders:
                    self.escribir_consola("[!] Borrando carpeta local : %s" % (folder_path,))
                    self.insertarTabla(list_name, "Archivo", "Borrado")
                    shutil.rmtree(folder_path)
            else:
                os.remove(folder_path)
                            
        self.escribir_consola("\n[+] Limpiando archivos")
            
        for folder in folders:
            if os.path.isdir(self.folder_pc + "/" + folder):
                files_pc = os.listdir(self.folder_pc + "/" + folder)
                for file_pc in files_pc:
                    file_found = False
                    for file_gd in self.tree_gd:
                        if folder == file_gd["folder"] and file_pc == file_gd["file"]:
                            file_found = True
                    if file_found == False:
                        filename_path = self.folder_pc + "/" + folder + "/" + file_pc
                        self.escribir_consola("[!] Borrando archivo local : %s" % (filename_path,))
                        self.insertarTabla(file_pc, "Directorio", "Borrado")
                        os.remove(filename_path)
                            

        self.escribir_consola("\n[+] Sincronizando Google Drive con archivos locales")

        for file_gd in self.tree_gd:
            
            id_drive = file_gd["id"]
            folder = file_gd["folder"]
            fullpath = self.folder_pc + "/" + file_gd["folder"]
            file = file_gd["file"]
            md5 = file_gd["md5"]
            
            filename = fullpath + "/" + file
            
            if not os.path.exists(fullpath):
                self.escribir_consola("[+] Creando nuevo directorio con nombre : %s" % (folder,))
                self.insertarTabla(folder, "Directorio", "Creado")
                os.makedirs(fullpath)
                
            self.downloadFile(id_drive, file, filename, md5)
            
        self.escribir_consola("\n[+] La sincronización con Google Drive se completó correctamente")

        self.sincronizarGD_btn.config(state=NORMAL)
        self.sincronizarPC_btn.config(state=NORMAL)

    def sync_from_pc(self):

        self.limpiar_tabla()
        self.limpiar_consola()

        self.escribir_consola("[+] Leyendo carpetas y archivos de Google Drive ...\n")
        
        id_folder_gd = self.get_folder_id_by_name(self.folder_gd_music)
                            
        self.list_folder_gd(id_folder_gd)
                
        folders = []
        
        for list_name in os.listdir(self.folder_pc):
            list_path = os.path.join(self.folder_pc, list_name)
            if os.path.isdir(list_path):
                folders.append(list_name)
                            
        folders = list(set(folders))

        # No existe nada, se crea todo desde cero
        
        if not self.tree_gd:
            
            self.escribir_consola("\n[+] No se encontro ningun archivo subido, se procede a subir todo el directorio local")

            for folder in folders:
                
                folders_gd = []
                
                files = os.listdir(self.folder_pc + "/" + folder)
                
                for file in files:
                
                    fullpath = self.folder_pc + "/" + folder + "/" + file
                
                    if not any(d['name'] == folder for d in folders_gd):
                        
                        new_id_folder = self.makeFolderDrive(id_folder_gd, folder)
                                            
                        folders_gd.append({ "id": new_id_folder, "name" : folder })
                                                                        
                    id_folder = next(filter(lambda x: x['name'] == folder,folders_gd))["id"]
                
                    self.uploadFile(id_folder, fullpath)
    
        # Si existe, se sincroniza
        
        if self.tree_gd:

            self.escribir_consola("\n[+] Sincronizando archivos locales con Google Drive")
            
            folders_gd = self.filterFolders()
                    
            # Se limpian carpetas que no existan en la nube pero si en la pc
            
            folders_deleted = []
            
            for folder_gd in folders_gd:
                if folder_gd not in folders:
                    id_folder = self.getIdByFolderName(folder_gd)
                    self.deleteFolderGD(id_folder,folder_gd)
                    folders_deleted.append(folder_gd)
            
            # Se borran los archivos que no existen en la nube pero si en la pc
            
            for folder_gd in folders_gd:
                if folder_gd not in folders_deleted:
                    local_files = self.filterLocalFilesFolder(folder_gd)
                    files_gd = self.filterFilesFolder(folder_gd)
                    for file_gd in files_gd:
                        id_drive = file_gd["id"]
                        filename = file_gd["file"]
                        if filename not in local_files:
                            #print("[+] Deleting file %s in folder %s" % (filename,folder_gd))
                            self.deleteFileGD(id_drive,filename)
            
            # Se sincronizan los directorios y archivos con la nube    
            
            for folder in folders:
                
                if folder not in folders_gd:
                    new_id_folder = self.makeFolderDrive(id_folder_gd, folder)
                    self.tree_folders_gd.append({ "id" : new_id_folder, "name" : folder })
                    
                id_folder = self.getIdByFolderName(folder)
                
                files_gd = self.filterFilesFolder(folder)
                            
                files = os.listdir(self.folder_pc + "/" + folder)
                
                for file in files:
                
                    fullpath = self.folder_pc + "/" + folder + "/" + file
                    
                    md5_file_pc = self.getMD5File(fullpath)
                    
                    fileFound = False
                    
                    for file_gd in files_gd:
                        id_drive = file_gd["id"]
                        folder_gd = file_gd["folder"]
                        filename_gd = file_gd["file"]
                        md5_gd = file_gd["md5"]
                        if filename_gd == file:
                            if md5_gd != md5_file_pc:
                                self.deleteFileGD(id_drive,file)
                                self.uploadFile(id_folder, fullpath)
                                
                            fileFound = True
                            
                    if fileFound == False:
                        self.uploadFile(id_folder, fullpath)
                    else:
                        self.insertarTabla(file, "Archivo", "Verificado")
                        
        self.escribir_consola("\n[+] La sincronización local se completó correctamente")

        self.sincronizarGD_btn.config(state=NORMAL)
        self.sincronizarPC_btn.config(state=NORMAL)

    def check_sync_from_gd(self):
        if self.folder_gd_music == "" or self.folder_gd_music == None:
            Messagebox.ok(message="Se debe configurar el directorio de Google Drive", parent = self)
        else:
            response = Messagebox.okcancel("Esta seguro de sincronizar con Google Drive ?", parent=self)
            if response == "OK":
                self.sincronizarGD_btn.config(state=DISABLED)
                self.sincronizarPC_btn.config(state=DISABLED)
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()
                self.drive = GoogleDrive(gauth)
                self.threadSync = threading.Thread(target=self.sync_from_drive())
                self.threadSync.start()

    def check_sync_from_pc(self):
        if self.folder_gd_music == "" or self.folder_gd_music == None:
            Messagebox.ok(message="Se debe configurar el directorio de Google Drive", parent = self)
        else:
            response = Messagebox.okcancel("Esta seguro de sincronizar desde la PC ?", parent=self)
            if response == "OK":
                self.sincronizarGD_btn.config(state=DISABLED)
                self.sincronizarPC_btn.config(state=DISABLED)
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()
                self.drive = GoogleDrive(gauth)
                self.threadSync = threading.Thread(target=self.sync_from_pc())
                self.threadSync.start()

    def cargarMenuSincronizacion(self, selfDash):

        self.selfDash = selfDash

        selfDash.ventana.destroy()

        selfDash.ventana = ttk.Frame(selfDash, bootstyle='secondary')
        selfDash.ventana.pack_propagate(0)
        selfDash.ventana.pack(side='left', fill='both', expand=True)

        self.tvArchivos = ttk.Treeview(
            selfDash.ventana,
            bootstyle='dark',
            show='headings',
            height=8,
            style='Files.Treeview',
        )
        
        self.tvArchivos.configure(columns=(
            'Nombre', 'Tipo', 'Estado'
        ))

        self.tvArchivos.column('Nombre', width=524, stretch=True, anchor='center')
        self.tvArchivos.column('Tipo', width=150, stretch=True, anchor='center')
        self.tvArchivos.column('Estado', width=500, stretch=True, anchor='center')
                
        for col in self.tvArchivos['columns']:
            self.tvArchivos.heading(col, text=col.title(), anchor='center')

        self.tvArchivos.place(x = 10, y = 10)
        
        scrollSync = ttk.Scrollbar(selfDash.ventana, orient="vertical", bootstyle='secondary', command=self.tvArchivos.yview)
        scrollSync.place(x = 1200, y = 13, height = 318)

        self.tvArchivos.configure(yscrollcommand=scrollSync.set)

        self.tvArchivos.unbind("<Button-1>")

        self.textConsole = ScrolledText(selfDash, padding=5, height=12, width=96, font=(None, 16), autohide=True, state="disabled")
        self.textConsole.place(x = 10, y = 420)

        self.sincronizarGD_btn = ttk.Button(selfDash, text="Sincronizar desde GD", width=20, command=self.check_sync_from_gd)
        self.sincronizarGD_btn.place(x = 340, y = 780)

        self.sincronizarPC_btn = ttk.Button(selfDash, text="Sincronizar desde PC", width=20, command=self.check_sync_from_pc)
        self.sincronizarPC_btn.place(x = 680, y = 780)

        self.limpiar_consola()