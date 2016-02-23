# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Updater
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#----------------------------------------------------------------------
import os
import json
import time
import re
from core import scrapertools
from core import config
from core import logger
from core import xmltools
from core.item import Item
from platformcode import platformtools

__channel__ = "updater"

headers = [["User-Agent", "pelisalacarta"]] 
repo = "divadres/pelisalacarta-oficial"
branch = "feature/servers"
GitApi = "https://api.github.com/repos/"+repo+"/contents/python/main-classic/%s?ref="+branch
DownloadUrl = "https://raw.githubusercontent.com/"+repo+"/"+branch+"/python/main-classic/"

def isGeneric():
    return True
    
def mainlist(item):
    itemlist = []
    itemlist.append(Item(action="refresh",title="Buscar actualizaciones...",channel =__channel__ ))
    updates = get_updates_list()
    if len(updates) > 0:
      #progress = platformtools.dialog_progress_bg("Pelisalacarta")   
      
      keys = sorted(updates, key = lambda key: (updates[key]["type"], updates[key]["name"]))
      for sha in keys:
        #progress.update((keys.index(sha)+1) *100 / len(updates),"Pelisalacarta", "Procesando: " + updates[sha]["name"][:-4] )
  
        #update =  get_update(sha)
        update = updates[sha]
        title = update["name"][:-4]
        if update["type"] =="channels":    title += " [C]"
        if update["type"] =="servers":     title += " [S]" 
        if update["change"] =="added":    title += " [N]"
        if update["change"] =="modified": title += " [U]"   
              
        itemlist.append(Item(action="download",title=title,channel =__channel__, extra=sha))
      #progress.close()
      
    if len(itemlist)>1:
      itemlist.insert(1,Item(action="download_all",title="Actualizar todo",channel =__channel__ ))
    else:
      itemlist.append(Item(title="¡No hay actualizaciones!"))
          
    return itemlist

def refresh(item):
  check_files(True)
  platformtools.itemlist_refresh()  

def download_all(item):
  time.sleep(1)
  download_all_updates()
  platformtools.dialog_ok("pelisalacarta","Descarga completada")
  platformtools.itemlist_refresh()
  
  
def download(item):
  sha = item.extra
  update  = get_update(sha)
  title = "%s v%s | %s" %(update["data"]["name"],update["data"]["version"],update["data"]["date"])
  info = "Cambios: %s" %(update["data"]["changes"])
  if platformtools.dialog_yesno(title,info):
    download_update(update) 
    platformtools.dialog_ok("pelisalacarta","Descarga completada")
    platformtools.itemlist_refresh()



def download_all_updates():
  progreso = platformtools.dialog_progress("Actualizando","")
  updates = read_updates()
  keys = sorted(updates, key = lambda key: updates[key]["name"])
  cantidad = len(updates)
  for sha in keys:
    #update  = get_update(sha) 
    update = updates[sha]
    percent = (keys.index(sha)+1) *100 / cantidad
    if progreso.iscanceled(): 
      progreso.close()
      return
    if update["type"] == "channels":
      progreso.update(percent,"Descargando canal: " + update["name"][:-4])
      download_update(update)
    if update["type"] == "servers":
      progreso.update(percent,"Descargando servidor: " + update["name"][:-4])
      download_update(update)
      
  progreso.close()

      
def download_update(update):
  xml, py = get_file_url(update)
  xmldata = download_file(xml["url"])
  pydata = download_file(py["url"])
  open(xml["path"],"wb").write(xmldata)
  open(py["path"],"wb").write(pydata)
  remove_update(update["sha"])
            


def download_file(url):
  for x in range(10):
    try:
      data = scrapertools.downloadpage(url)
      assert data
      return data
    except:
      logger.info("No se ha podido descargar: " + url + " (intento " + str(x) + " de 10)" )
    else:
      break
  else:
      logger.info("Ha sido imposible descargar: " + url)
      logger.info("Abortando")
      raise Exception("File not downloaded")
      

def read_updates():
  if os.path.exists(os.path.join(config.get_data_path(),"updates.json")):
    try:
      updates=json.loads(open(os.path.join(config.get_data_path(),"updates.json"),"r").read())
    except:
      updates = {}
  else:
    updates = {}
  return updates

def add_update(update, change, type):
  updates = read_updates()
  if not update["sha"] in updates:
    updates[update["sha"]] = {}
    updates[update["sha"]]["name"] = update["name"]
    updates[update["sha"]]["sha"] = update["sha"]
    updates[update["sha"]]["change"] = change
    updates[update["sha"]]["type"] = type
    open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(updates, indent=4, sort_keys=True))
    
    
def remove_update(sha):
  updates = read_updates()
  if sha in updates:
   del updates[sha]
   open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(updates, indent=4, sort_keys=True))

def get_file_url(update):
  urls = []
  if "data" in update:
    base_url =  update["data"]["update_url"]
    base_url=""
  else:
    base_url =""
  if not base_url: base_url = DownloadUrl + update["type"] + "/"
  
  if "data" in update:
    xmlfile = update["data"]["id"]+".xml"
    pyfile = update["data"]["id"]+".py"
  else:
    xmlfile = update["name"]
    pyfile = update["name"].replace(".xml",".py")

  xml = {"url": base_url + xmlfile, "path": os.path.join(config.get_runtime_path(),update["type"], xmlfile)}
  py = {"url": base_url + pyfile, "path": os.path.join(config.get_runtime_path(),update["type"], pyfile)}
  
  return xml, py

  
def get_update(sha):
  updates = read_updates()
  if not "data" in updates[sha]:
    xml, py = get_file_url(updates[sha])
    xmldata = scrapertools.downloadpage(xml["url"])
    xmldata = unicode(xmldata,"utf8","ignore").encode("utf8")
    dct_data = xmltools.xml2dict(xmldata=xmldata)
    updates[sha]["data"] = dct_data[dct_data.keys()[0]]
    open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(updates, indent=4, sort_keys=True))
  return updates[sha]
  
def get_updates_list():
  updates = read_updates()
  channel_list = get_file_list("channels")
  server_list = get_file_list("servers")
  shas = updates.keys()
  for sha in shas:
    if updates[sha]["type"]=="channels":
      if updates[sha]["change"]=="added" and updates[sha]["name"] in channel_list:
        updates[sha]["change"]="modified"
      if updates[sha]["change"]=="modified" and not updates[sha]["name"] in channel_list:
        updates[sha]["change"]="added"
      if updates[sha]["change"]=="modified" and channel_list[updates[sha]["name"]]["sha"] == sha:
        del updates[sha]
      continue
    if updates[sha]["type"]=="servers":
      if updates[sha]["change"]=="added" and updates[sha]["name"] in server_list:
        updates[sha]["change"]="modified"
      if updates[sha]["change"]=="modified" and not updates[sha]["name"] in server_list:
        updates[sha]["change"]="added"
      if updates[sha]["change"]=="modified" and server_list[updates[sha]["name"]]["sha"] == sha:
        del updates[sha]

  open(os.path.join(config.get_data_path(),"updates.json"),"w").write(json.dumps(updates, indent=4, sort_keys=True))
  return updates
 
 
def checkforupdates():
  from threading import Thread
  Thread(target=threaded_checkforupdates).start()

def threaded_checkforupdates():
  logger.info("checkforupdates")
  import time
  #Actualizaciones del plugin
  if config.get_setting("updateplugin") == "true":
    logger.info("Comprobando actualizaciones de pelisalcarta")
    
    LOCAL_VERSION_FILE = open(os.path.join(config.get_runtime_path(), "version.xml" )).read()
    #REMOTE_VERSION_FILE = scrapertools.downloadpage(DownloadUrl % "bin/version.xml")
    REMOTE_VERSION_FILE = scrapertools.downloadpage("http://descargas.tvalacarta.info/pelisalacarta-version.xml")
    
    try:
      versiondescargada = scrapertools.get_match(REMOTE_VERSION_FILE,"<tag>([^<]+)</tag").strip()
    except:
      versiondescargada = "0.0.0"
      
    versionlocal = scrapertools.get_match(LOCAL_VERSION_FILE,"<tag>([^<]+)</tag")  
        
    logger.info("Versión local: " + versionlocal)
    logger.info("Versión remota: " + versiondescargada)
    
    from distutils.version import StrictVersion
    if StrictVersion(versiondescargada) > StrictVersion(versionlocal):
      if platformtools.dialog_yesno("pelisalacarta","¡Hay una nueva versión lista para descargar!\nVersión actual: "+versionlocal+" - Nueva versión: "+versiondescargada+"\nQuieres instalarla ahora?"):
        update(versiondescargada)
        return
      else:
       logger.info("Opción seleccionada: No Descargar")
  #Actualizacion de canales      
  if config.get_setting("updatechannels") =="1" or config.get_setting("updatechannels") =="2":
    check_files()

def check_files(channelmode=False):
  logger.info("pelisalacarta.core.updates check_files")
  progress = platformtools.dialog_progress_bg("Pelisalacarta","Comprobando actualizaciones...")
  progress.update(50, "Pelisalacarta","Descargando lista de canales...")
  
  api_data = scrapertools.downloadpage(GitApi %("channels"), headers=headers)
  RemoteJSONData = json.loads(api_data)
  LocalJSONData = get_file_list("channels")
  

  for file in RemoteJSONData:
    if file["name"].endswith(".xml"):
      if not file["name"] in LocalJSONData:
        add_update(file, "added", "channels")
      elif file["sha"] <> LocalJSONData[file["name"]]["sha"]:
        add_update(file, "modified", "channels")
        
  progress.update(100, "Pelisalacarta", "Descargando lista de servidores...")
  
  api_data = scrapertools.downloadpage(GitApi %("servers"), headers=headers)
  RemoteJSONData = json.loads(api_data)
  LocalJSONData = get_file_list("servers")
  
  for file in RemoteJSONData:
    if file["name"].endswith(".xml"):
      if not file["name"] in LocalJSONData:
        add_update(file, "added", "servers")
      elif file["sha"] <> LocalJSONData[file["name"]]["sha"]:
        add_update(file, "modified", "servers")

  if channelmode: 
    progress.close()
    return
  
  #Si todo esta al dia:
  updates = get_updates_list()
  if len(updates) == 0:
    progress.update(100, "Pelisalacarta","Todos los canales y servidores estan actualizados")
    time.sleep(1)
    progress.close()
        
  #Si hay actualizaciones
  else:
    progress.update(100, "Pelisalacarta", "Hay actualizaciones disponibles")
    time.sleep(1)
    progress.close()
      
    if config.get_setting("updatechannels") =="1": #Automatico
      download_all_updates()
         
    elif config.get_setting("updatechannels") =="2": #Preguntar
      if platformtools.dialog_yesno("pelisalacarta","¡Hay "+str(len(updates)) + " actualizaciones disponibles\nQuieres instalarlas ahora?"):
        download_all_updates()

def get_file_list(path):
  logger.info("pelisalacarta.core.updates get_file_list")
  path = os.path.join(config.get_runtime_path(),path)
  logger.info("pelisalacarta.core.updates get_file_list path=" + path)
  import hashlib
  list={}
  for file in os.listdir(path):
    if file.endswith(".xml"):
        data = open(os.path.join(path,file), 'rb').read()
        dct_data = xmltools.xml2dict(xmldata=data)
        list[os.path.basename(file)] = {}
        list[os.path.basename(file)]["sha"] = hashlib.sha1("blob " + str(len(data)) + "\0" + data).hexdigest()
        list[os.path.basename(file)]["changes"] = dct_data[dct_data.keys()[0]]["changes"]
        list[os.path.basename(file)]["date"] = dct_data[dct_data.keys()[0]]["date"]
        list[os.path.basename(file)]["version"] = dct_data[dct_data.keys()[0]]["version"]
        list[os.path.basename(file)]["name"] = dct_data[dct_data.keys()[0]]["name"]
        list[os.path.basename(file)]["id"] = dct_data[dct_data.keys()[0]]["id"]
        list[os.path.basename(file)]["update_url"] = dct_data[dct_data.keys()[0]]["update_url"]
        
  return list

  
def GetDownloadPath(version, platform=""):
  zipfile = config.PLUGIN_NAME + "-%s-%s.zip"
  if not platform:
    if config.PLATFORM_NAME=="xbmc":
        platform = "xbmc-plugin"
    else:
        platform = config.PLATFORM_NAME
  return zipfile % (platform, version)
  
  

def update(version):
    logger.info("Actualizando plugin...")   
    
    LOCAL_FILE = os.path.join( config.get_data_path(),"pelisalacarta.zip" )

    REMOTE_FILE = "http://descargas.tvalacarta.info/" + GetDownloadPath(version)
    DESTINATION_FOLDER = os.path.join(config.get_runtime_path(),"..")

    logger.info("Archivo Remoto: " + REMOTE_FILE)
    logger.info("Archivo Local: " + LOCAL_FILE)
    
    from core import downloadtools
    if os.path.isfile(LOCAL_FILE):
      os.remove(LOCAL_FILE)
      
    ret = downloadtools.downloadfile(REMOTE_FILE, LOCAL_FILE)
    
    if ret is None:
      logger.info("Descomprimiendo fichero...")
      import ziptools
      unzipper = ziptools.ziptools()
      logger.info("Destino: " + DESTINATION_FOLDER)


      import shutil
      for file in os.listdir(os.path.join(config.get_runtime_path())):
        if not file in [".",".."]:
          if os.path.isdir(os.path.join(config.get_runtime_path(), file)):
            shutil.rmtree(os.path.join(config.get_runtime_path(), file))
          if os.path.isfile(os.path.join(config.get_runtime_path(), file)):
            os.remove(os.path.join(config.get_runtime_path(), file))
     
      unzipper.extract(LOCAL_FILE,DESTINATION_FOLDER)
      os.remove(LOCAL_FILE)
      platformtools.dialog_ok("Actualizacion", "Pelisalacarta se ha actualizado correctamente")
    elif ret == -1:
      platformtools.dialog_ok("Actualizacion", "Descarga Cancelada")
    else:
      platformtools.dialog_ok("Actualizacion", "Se ha producido un error al descargar el archivo")
