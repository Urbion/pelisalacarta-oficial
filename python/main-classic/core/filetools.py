# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# filetools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#Gestion de archivos con discriminación samba/local
import os
from lib.samba import libsmb as samba

def read(path):
    '''
    Lee el contenido de un archivo y devuelve los datos
    '''
    if path.lower().startswith("smb://"):
      return samba.get_file_handle_for_reading(os.path.basename(path), os.path.dirname(path)).read()
    else:
      return open(path, "rb").read()


def write(path, data):
    '''
    Guarda los datos en un archivo
    '''
    if path.lower().startswith("smb://"):
      samba.store_file(os.path.basename(path), data, os.path.dirname(path))
    else:
      open(path, "wb").write(data)


def open_for_reading(path):
    '''
    Abre un archivo para leerlo
    '''
    if path.lower().startswith("smb://"):
      
      return samba.get_file_handle_for_reading(os.path.basename(path), os.path.dirname(path))
    else:
      return open(path, "rb") 


def exists(path):
    '''
    Retorna True si la ruta existe, tanto si es una carpeta como un archivo
    '''
    if path.lower().startswith("smb://"):
      return samba.file_exists(os.path.basename(path), os.path.dirname(path)) or samba.folder_exists(os.path.basename(path), os.path.dirname(path))
    else:
      return os.path.exists(path)
    
    
def isfile(path):
    '''
    Retorna True si la ruta existe y es un archivo
    '''
    if path.lower().startswith("smb://"):
      return samba.file_exists(os.path.basename(path), os.path.dirname(path))
    else:
      return os.path.isfile(path)


def getsize(path):
    '''
    Obtiene el tamaño de un archivo
    '''
    if path.lower().startswith("smb://"):
      return samba.get_attributes(os.path.basename(path), os.path.dirname(path)).file_size 
    else:
      return os.path.getsize(path)


def remove(path):
    '''
    Elimina un archivo
    '''
    if path.lower().startswith("smb://"):
      samba.delete_files(os.path.basename(path), os.path.dirname(path))
    else:
      os.remove(path)


def rmdir(path):
    '''
    Elimina un directorio
    '''
    if path.lower().startswith("smb://"):
      samba.delete_directory(os.path.basename(path), os.path.dirname(path))
    else:
      os.rmdir(path)


def mkdir(path):
    '''
    Crea un directorio
    '''
    if path.lower().startswith("smb://"):
      samba.create_directory(os.path.basename(path), os.path.dirname(path))
    else:
      os.mkdir(path)
    

def listdir(path):
    '''
    Lista un directorio
    '''
    if path.lower().startswith("smb://"):
      files, directories = samba.get_files_and_directories(os.path.basename(path), os.path.dirname(path))
      return files + directories
    else:
      return os.listdir(path)