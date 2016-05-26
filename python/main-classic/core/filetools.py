# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# filetools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#Gestion de archivos con discriminación samba/local

def read(path):
    '''
    Lee el contenido de un archivo y devuelve los datos
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      return samba.get_file_handle_for_reading(os.path.basename(path), os.path.dirname(path)).read()
    else:
      return open(path, "rb").read()


def write(path, data):
    '''
    Guarda los datos en un archivo
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      samba.store_file(os.path.basename(path), data, os.path.dirname(path))
    else:
      open(path, "wb").write(data)


def exists(path):
    '''
    Retorna True si la ruta existe, tanto si es una carpeta como un archivo
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      return samba.file_exists(os.path.basename(path), os.path.dirname(path)) or samba.folder_exists(os.path.basename(path), os.path.dirname(path))
    else:
      import os
      return os.path.exists(path)
    
    
def isfile(path):
    '''
    Retorna True si la ruta existe y es un archivo
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      return samba.file_exists(os.path.basename(path), os.path.dirname(path))
    else:
      import os
      return os.path.isfile(path)


def remove(path):
    '''
    Elimina un archivo
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      samba.delete_files(os.path.basename(path), os.path.dirname(path))
    else:
      import os
      os.remove(path)


def rmdir(path):
    '''
    Elimina un directorio
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      samba.delete_directory(os.path.basename(path), os.path.dirname(path))
    else:
      import os
      os.rmdir(path)


def mkdir(path):
    '''
    Crea un directorio
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      samba.create_directory(os.path.basename(path), os.path.dirname(path))
    else:
      import os
      os.mkdir(path)
    

def listdir(path):
    '''
    Lista un directorio
    '''
    if path.lower().startswith("smb://"):
      from lib.samba import libsmb as samba
      files, directories = samba.delete_directory(os.path.basename(path), os.path.dirname(path))
      return files + directories
    else:
      import os
      return os.listdir(path)