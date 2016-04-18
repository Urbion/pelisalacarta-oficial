# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para HTML
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys, os
from core import config
from core import logger
from controller import Controller
from controller import Platformtools
from platformcode import platformtools
import json
import re
from core.item import Item
import threading
import random
from platformcode import launcher

class html(Controller):
  pattern = re.compile("##")
  name = "HTML"
  
  def __init__(self, handler=None):
    super(html,self).__init__(handler)
    self.platformtools = platform(self)
    self.data = {}
    
    if self.handler:
      self.client_ip = handler.client.getpeername()[0]
      ID = "%032x" %(random.getrandbits(128))
      self.handler.sendMessage('{"action": "connect", "data":{"version": "pelisalacarta '+config.get_plugin_version()+'", "date":"'+config.get_plugin_date()+'"}, "id": "'+ ID +'"}')
      launcher.start()
    
  def extract_item(self,path):
      if path:
        item = Item()
        item.fromurl(path)
      else:
        item = Item(channel="channelselector", action="mainlist")
      return item
    
  def run(self, path):    
      item = self.extract_item(path)
      launcher.run(item)

  def set_data(self, data):
    self.data = data
    
  def get_data(self, id):
    if "id" in self.data and self.data["id"] == id:
      data = self.data["result"]
    else:
      data = None
    return data
    
  def send_message(self, data):
    import random
    
    ID = "%032x" %(random.getrandbits(128))
    data["id"] = ID
    
    platformtools.controllers[threading.current_thread().name].handler.sendMessage(json.dumps(data))
    return ID

 
class platform(Platformtools):
  def __init__(self, controller):
    self.item_list = []
    self.controller = controller
    self.handler = controller.handler
    self.get_data = controller.get_data
    self.send_message = controller.send_message

    
  def AddNewItem(self,item, totalItems=0):
    item.title = unicode(item.title, "utf8", "ignore").encode("utf8")
    item.fulltitle = unicode(item.fulltitle, "utf8", "ignore").encode("utf8")
    item.plot = unicode(item.plot, "utf8", "ignore").encode("utf8")

    contextCommands = []
    if type(item.context) == list:
      for context in item.context:
        contextitem = item.clone()
        contextitem.action = context["action"]
        contextitem.item_action = item.action
        if "channel" in context and context["channel"]:
          contextitem.channel = context["channel"]
        contextCommands.append([context["title"],contextitem.tourl()])
   

    JsonItem = {}
    JsonItem["title"]=item.title
    JsonItem["thumbnail"]= item.thumbnail
    JsonItem["fanart"]=item.fanart
    JsonItem["plot"]=item.plot
    JsonItem["action"]=item.action
    JsonItem["url"]=item.tourl()
    JsonItem["context"]=[]
    for Comando in contextCommands:
      JsonItem["context"].append({"title":Comando[0],"url": Comando[1]})
    self.item_list.append(JsonItem)
         
         
  def render_items(self, itemlist, parentitem):
    from core.item import Item
        
    if (parentitem.channel=="channelselector" and parentitem.action=="mainlist") or (parentitem.channel=="novedades" and parentitem.action=="mainlist") or (parentitem.channel=="buscador" and parentitem.action=="mainlist") or (parentitem.channel=="channelselector" and parentitem.action=="channeltypes"):
      viewmode = 0
    elif parentitem.channel=="channelselector" and parentitem.action=="listchannels":
      viewmode = 1
    else:
      viewmode = 2
    
    if not (parentitem.channel=="channelselector" and parentitem.action=="mainlist") and not itemlist[0].action=="go_back":
      if viewmode !=2:
        itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","bannermenu","thumb_atras.png")))
      else:
        itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","squares","thumb_atras.png")))
           
    for item in itemlist:
        if item.thumbnail == "" and item.action == "search": item.thumbnail = config.get_thumbnail_path() + "thumb_buscar.png"
        if item.thumbnail == "" and item.folder == True: item.thumbnail = "http://media.tvalacarta.info/pelisalacarta/thumb_folder.png"
        if item.thumbnail == "" and item.folder == False: item.thumbnail = "http://media.tvalacarta.info/pelisalacarta/thumb_nofolder.png"
        
        if "http://media.tvalacarta.info/" in item.thumbnail and not item.thumbnail.startswith("http://media.tvalacarta.info/pelisalacarta/thumb_"):
          if viewmode != 2: 
            item.thumbnail = config.get_thumbnail_path("bannermenu") + os.path.basename(item.thumbnail)
          else:
            item.thumbnail = config.get_thumbnail_path() + os.path.basename(item.thumbnail)
        
        #Estas imagenes no estan en bannermenu, asi que si queremos bannermenu, para que no se vean mal las quitamos    
        elif viewmode != 2 and item.thumbnail.startswith("http://media.tvalacarta.info/pelisalacarta/thumb_"):
          item.thumbnail = ""
            
        if item.fanart == "":
            channel_fanart = os.path.join(config.get_runtime_path(), 'resources', 'images', 'fanart', item.channel + '.jpg')
            if os.path.exists(channel_fanart):
                item.fanart = channel_fanart
            else:
                item.fanart = os.path.join(config.get_runtime_path(), "fanart.jpg")

        if item.category == "":
            item.category = parentitem.category

        if item.fulltitle == "":
            item.fulltitle = item.title

        self.AddNewItem(item, totalItems=len(itemlist))
        

    JsonData = {}
    JsonData["action"]="EndItems"
    JsonData["data"]={}
    JsonData["data"]["itemlist"]=self.item_list
    JsonData["data"]["mode"]=viewmode   
    JsonData["data"]["host"]=self.controller.host

    ID = self.send_message(JsonData)
    self.item_list= []
    while self.get_data(ID) == None:
      continue


  def dialog_ok(self, heading, line1, line2="", line3=""):
      text = line1
      if line2: text += "\n" + line2
      if line3: text += "\n" + line3
      JsonData = {}
      JsonData["action"]="Alert" 
      JsonData["data"]={}
      JsonData["data"]["title"]=heading
      JsonData["data"]["text"]=unicode(text ,"utf8","ignore").encode("utf8")
      ID = self.send_message(JsonData)
      while  self.get_data(ID) == None:
        continue
    
  def dialog_notification(self, heading, message, icon=0, time=5000, sound=True):
      #No disponible por ahora, muestra un dialog_ok
      self.dialog_ok(heading,message)

  def dialog_yesno(self, heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
      text = line1
      if line2: text += "\n" + line2
      if line3: text += "\n" + line3
      JsonData = {}
      JsonData["action"]="AlertYesNo" 
      JsonData["data"]={}
      JsonData["data"]["title"]=heading
      JsonData["data"]["text"]=text
      ID = self.send_message(JsonData)
      while self.get_data(ID) == None:
        continue

      return self.get_data(ID)
    
  def dialog_select(self, heading, list): 
      JsonData = {}
      JsonData["action"]="List"
      JsonData["data"]={}
      JsonData["data"]["title"]=heading
      JsonData["data"]["list"]=[]
      for Elemento in list:
        JsonData["data"]["list"].append(Elemento)
      ID = self.send_message(JsonData)
      while self.get_data(ID) == None:
        continue
      return self.get_data(ID)
    
  def dialog_progress(self, heading, line1, line2="", line3=""):
      class Dialog(object):
          def __init__(self, heading, line1, line2, line3, platformtools):
              self.platformtools = platformtools
              self.closed = False
              self.heading = heading
              text = line1
              if line2: text += "\n" + line2
              if line3: text += "\n" + line3
              
              JsonData = {}
              JsonData["action"]="Progress" 
              JsonData["data"]={}
              JsonData["data"]["title"]=heading
              JsonData["data"]["text"]=text
              JsonData["data"]["percent"]=0
              
              ID = self.platformtools.send_message(JsonData)
              while self.platformtools.get_data(ID) == None:
                continue


          def iscanceled(self):
              JsonData = {}
              JsonData["action"]="ProgressIsCanceled" 
              JsonData["data"]={}
              ID = self.platformtools.send_message(JsonData)
              while self.platformtools.get_data(ID) == None:
                continue
                
              return self.platformtools.get_data(ID)

          def update(self, percent, line1, line2="", line3=""):
              text = line1
              if line2: text += "\n" + line2
              if line3: text += "\n" + line3
              JsonData = {}
              JsonData["action"]="ProgressUpdate" 
              JsonData["data"]={}
              JsonData["data"]["title"]=self.heading
              JsonData["data"]["text"]=text
              JsonData["data"]["percent"]=percent
              self.platformtools.send_message(JsonData)

          def close(self):
              JsonData = {}
              JsonData["action"]="ProgressClose" 
              JsonData["data"]={}
              ID = self.platformtools.send_message(JsonData)
              while self.platformtools.get_data(ID) == None:
                continue
              self.closed = True

      return Dialog(heading, line1, line2, line3, self)


  def dialog_progress_bg(self, heading, message=""):
      class Dialog(object):
          def __init__(self, heading, message, platformtools):
              self.platformtools = platformtools
              self.closed = False
              self.heading = heading
              JsonData = {}
              JsonData["action"]="ProgressBG" 
              JsonData["data"]={}
              JsonData["data"]["title"]=heading
              JsonData["data"]["text"]=message
              JsonData["data"]["percent"]=0
              
              ID = self.platformtools.send_message(JsonData)
              while self.platformtools.get_data(ID) == None:
                continue

          def isFinished(self):
              return not self.closed

          def update(self, percent=0, heading="", message=""):
              JsonData = {}
              JsonData["action"]="ProgressBGUpdate" 
              JsonData["data"]={}
              JsonData["data"]["title"]=heading
              JsonData["data"]["text"]=message
              JsonData["data"]["percent"]=percent
              self.platformtools.send_message(JsonData)

          def close(self):
              JsonData = {}
              JsonData["action"]="ProgressBGClose" 
              JsonData["data"]={}
              ID = self.platformtools.send_message(JsonData)
              while self.platformtools.get_data(ID) == None:
                continue
              self.closed = True
              
      return Dialog(heading, message, self)

  def dialog_input(self, default="", heading="", hidden=False):
      JsonData = {}
      JsonData["action"]="Keyboard" 
      JsonData["data"]={}
      JsonData["data"]["title"]=heading
      JsonData["data"]["text"]=default
      JsonData["data"]["password"]=hidden
      ID = self.send_message(JsonData)
      while self.get_data(ID) == None:
        continue
      return self.get_data(ID)

  def dialog_numeric(self, type, heading, default=""):
      return self.dialog_input("", heading, False) 

  def itemlist_refresh(self):
      JsonData = {}
      JsonData["action"]="Refresh" 
      JsonData["data"]={}
      ID = self.send_message(JsonData)
      while self.get_data(ID) == None:
        continue

  def itemlist_update(self, item):
      JsonData = {}
      JsonData["action"]="Update" 
      JsonData["data"]={}
      JsonData["data"]["url"]=item.tourl()
      ID = self.send_message(JsonData)

      while self.get_data(ID) == None:
        continue

  def is_playing(self):
    JsonData = {}
    JsonData["action"]="isPlaying" 
    JsonData["data"]={}
    ID = self.send_message(JsonData)
    while self.get_data(ID)== None:
      continue
    return self.get_data(ID)

  def play_video(self, item):
      if item.contentTitle:
        title = item.contentTitle
      elif item.fulltitle:
        title = item.fulltitle
      else:
        title = item.title
      
      if item.contentPlot:
        plot = item.contentPlot
      else:
        plot = item.plot  
      JsonData = {}
      JsonData["action"]="Play" 
      JsonData["data"]={}
      JsonData["data"]["title"]= title
      JsonData["data"]["plot"]= plot
      JsonData["data"]["video_url"] =  item.video_url
      JsonData["data"]["url"] =  item.url
      JsonData["data"]["host"] =  self.controller.host
      ID = self.send_message(JsonData)
      while self.get_data(ID) == None:
        continue
   
  def open_settings(self,items):
    from core import config
    JsonData = {}
    JsonData["action"]="OpenConfig"   
    JsonData["data"]={}
    JsonData["data"]["title"]= "Opciones"
    JsonData["data"]["items"]=[]
    
    for item in items:
      for key in item:
        if key in ["lvalues", "label", "category"]:
          try:
            ops = item[key].split("|")
            for x, op in enumerate(ops):
              ops[x] = config.get_localized_string(int(ops[x])) 
            item[key] = "|".join(ops)
          except:
            pass

      JsonData["data"]["items"].append(item)
    ID = self.send_message(JsonData)

    while self.get_data(ID) == None:
      pass
      
    if self.get_data(ID):
      from core import config
      config.set_settings(self.get_data(ID))
      JsonData = {}
    JsonData["action"]="HideLoading"
    JsonData["data"] = {}
    self.send_message(JsonData)

  def show_channel_settings(self, list_controls=None, dict_values=None, caption="", callback=None, item=None):
    from core import config
    from core import channeltools
    import inspect
    if not os.path.isdir(os.path.join(config.get_data_path(), "settings_channels")):
       os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))
       
              
    title = caption


    #Obtenemos el canal desde donde se ha echo la llamada y cargamos los settings disponibles para ese canal
    channelpath = inspect.currentframe().f_back.f_back.f_code.co_filename
    channelname = os.path.basename(channelpath).replace(".py", "")

    #Si no tenemos list_controls, hay que sacarlos del xml del canal
    if not list_controls:      
    
      #Si la ruta del canal esta en la carpeta "channels", obtenemos los controles y valores mediante chaneltools
      if os.path.join(config.get_runtime_path(), "channels") in channelpath:
      
        # La llamada se hace desde un canal
        list_controls, default_values = channeltools.get_channel_controls_settings(channelname)

      #En caso contrario salimos
      else:
        return None


    #Si no se pasan dict_values, creamos un dict en blanco
    if  dict_values == None:
      dict_values = {}
    
    #Ponemos el titulo
    if caption =="": 
      caption = str(config.get_localized_string(30100)) + " -- " + channelname.capitalize()
    elif caption.startswith('@') and unicode(caption[1:]).isnumeric():
        caption = config.get_localized_string(int(caption[1:]))
    
    
  
    JsonData = {}
    JsonData["action"]="OpenConfig"   
    JsonData["data"]={}
    JsonData["data"]["title"]=caption
    JsonData["data"]["items"]=[]
    

    # Añadir controles
    for c in list_controls:
        if not "default" in c: c["default"] = ""
        if not "color" in c: c["color"] = "auto"
        
        #Obtenemos el valor
        if not c["id"] in dict_values:
          if not callback:
            c["value"]= config.get_setting(c["id"],channelname)
          else:
            c["value"] = c["default"]

          
        # Translation
        if c['label'].startswith('@') and unicode(c['label'][1:]).isnumeric():
            c['label'] = str(config.get_localized_string(c['label'][1:]))
        if c["label"].endswith (":"): c["label"] = c["label"][:-1]
        
        if c['type'] == 'list':
            lvalues=[]
            for li in c['lvalues']:
                if li.startswith('@') and unicode(li[1:]).isnumeric():
                    lvalues.append(str(config.get_localized_string(li[1:])))
                else:
                    lvalues.append(li)
            c['lvalues'] = lvalues

        JsonData["data"]["items"].append(c)
      
    ID = self.send_message(JsonData)

    while self.get_data(ID) == None:
      pass
    data = self.get_data(ID)
    
    JsonData["action"]="HideLoading"
    JsonData["data"] = {}
    self.send_message(JsonData)
    if not data == False:
      for v in data:
          if data[v] == "true": data[v] = True
          if data[v] == "false": data[v] = False
          if unicode(data[v]).isnumeric():  data[v] =  int(data[v])
        
      if not callback:
        for v in data:
          config.set_setting(v,data[v],channelname)
      else:
        exec "from channels import " + channelname + " as cb_channel"
        exec "return_value = cb_channel." + callback + "(item, data)"
        return return_value

        
    

     

    