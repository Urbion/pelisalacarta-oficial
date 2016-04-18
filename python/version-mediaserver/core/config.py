# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os,re
import logger
PLATFORM_NAME="mediaserver"
PLUGIN_NAME="pelisalacarta"

settings_dic ={}
def is_xbmc():
    return False

def get_library_support():
    return False

def get_platform():
  return PLATFORM_NAME
  
def get_system_platform():
    return "mediaserver"
    
def get_local_ip():
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 53))  # connecting to a UDP address doesn't send packets
  myip = s.getsockname()[0]
  return myip

def get_plugin_version():
    data = open(os.path.join(get_runtime_path(),"version.xml"),"r").read()
    return data.split("<tag>")[1].split("</tag>")[0]

def get_plugin_date():
    data = open(os.path.join(get_runtime_path(),"version.xml"),"r").read()
    return data.split("<date>")[1].split("</date>")[0]

def open_settings():
    Opciones =[]
    from xml.dom import minidom
    settings = open(menufilepath, 'rb').read()
    xmldoc= minidom.parseString(settings)
    for category in xmldoc.getElementsByTagName("category"):
      for setting in category.getElementsByTagName("setting"):
        Opciones.append(dict(setting.attributes.items() + [(u"category",category.getAttribute("label")),(u"value",get_setting(setting.getAttribute("id")))]))

    from platformcode import platformtools
    platformtools.open_settings(Opciones)

 
def get_setting(name,channel=""):
    if channel:
      from core import channeltools
      value = channeltools.get_channel_setting(name, channel)
      if not value is None:
        return value       
         
    global settings_dic
    if name in settings_dic:
      return settings_dic[name]
    else:
      return ""

    
def load_settings():
    global settings_dic
    defaults = {}
    from xml.etree import ElementTree
    settings=""
    encontrado = False
    #Lee el archivo XML (si existe)
    if os.path.exists(configfilepath):
      while len(settings)<> os.path.getsize(configfilepath) or len(settings)==0:
        settings = open(configfilepath, 'rb').read()
      root = ElementTree.fromstring(settings)
      for target in root.findall("setting"):
        settings_dic[target.get("id")] = target.get("value")

          

    defaultsettings=""
    while len(defaultsettings)<> os.path.getsize(menufilepath) or len(defaultsettings)==0:
      defaultsettings = open(menufilepath, 'rb').read()
    root = ElementTree.fromstring(defaultsettings)
    for category in root.findall("category"):
      for target in category.findall("setting"):
        if target.get("id"):
          defaults[target.get("id")] = target.get("default")
      
    for key in defaults:
      if not key in settings_dic:
        settings_dic[key] =  defaults[key]
    set_settings(settings_dic)


def set_setting(name,value,channel=""):
    if channel:
      from core import channeltools
      return channeltools.set_channel_setting(name,value, channel)
      
    else:     
      settings_dic[name]=value
      from xml.dom import minidom
      #Crea un Nuevo XML vacio
      new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
      new_settings_root = new_settings.documentElement
      
      for key in settings_dic:
        nodo = new_settings.createElement("setting")
        nodo.setAttribute("value",settings_dic[key])
        nodo.setAttribute("id",key)    
        new_settings_root.appendChild(nodo)
        
      fichero = open(configfilepath, "w")
      fichero.write(new_settings.toprettyxml(encoding='utf-8'))
      fichero.close()

def set_settings(JsonRespuesta):
    for Ajuste in JsonRespuesta:
      settings_dic[Ajuste]=JsonRespuesta[Ajuste].encode("utf8")
    from xml.dom import minidom
    #Crea un Nuevo XML vacio
    new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
    new_settings_root = new_settings.documentElement
    
    for key in settings_dic:
      nodo = new_settings.createElement("setting")
      nodo.setAttribute("value",settings_dic[key])
      nodo.setAttribute("id",key)    
      new_settings_root.appendChild(nodo)
      
    fichero = open(configfilepath, "w")
    fichero.write(new_settings.toprettyxml(encoding='utf-8'))
    fichero.close()
    


def get_localized_string(code):
    translationsfile = open(TRANSLATION_FILE_PATH,"r")
    translations = translationsfile.read()
    translationsfile.close()
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code

def get_data_path():
    return os.path.join( os.path.expanduser("~") , ".pelisalacarta" )

def get_runtime_path():
    return os.getcwd()
# Test if all the required directories are created
def verify_directories_created():
    logger.info("Comprobando directorios")
    if not os.path.exists(get_data_path()): os.mkdir(get_data_path())
    
    config_paths = [["library_path",     "Library"],
                    ["downloadpath",     "Downloads"],
                    ["downloadlistpath", os.path.join("Downloads","List")],
                    ["bookmarkpath",     "Favorites"]]
                             
    for setting, default in config_paths:
      path = get_setting(setting)
      if path=="":
          path = os.path.join( get_data_path() , default)
          set_setting(setting , path)
          
      if not get_setting(setting).lower().startswith("smb") and not os.path.exists(get_setting(setting)):
        os.mkdir(get_setting(setting))
                    
            
def get_thumbnail_path(preferred_thumb=""):
    WEB_PATH = ""
    
    if preferred_thumb=="":
        thumbnail_type = get_setting("thumbnail_type")
        if thumbnail_type=="": thumbnail_type="2"
        
        if thumbnail_type=="0":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/squares/"
    else:
        WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/"+preferred_thumb+"/"
        
    return WEB_PATH
    
# Fichero de configuración
menufilepath= os.path.join(get_runtime_path(),"resources", "settings.xml")
configfilepath = os.path.join( get_data_path() , "settings.xml")
if not os.path.exists(get_data_path()): os.mkdir(get_data_path())   
# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
load_settings()