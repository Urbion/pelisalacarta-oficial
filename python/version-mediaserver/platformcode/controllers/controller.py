# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador generico
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
from core import config
from platformcode import platformtools
import threading
class Controller(object):
    pattern = ""
    name = None
    client_ip = None
    def __init__(self, handler = None):
        self.handler = handler
        self.platformtools = Platformtools()
        self.host = "http://"+ config.get_local_ip() +":" + config.get_setting("server.port")
        if self.handler:
           platformtools.controllers[threading.current_thread().name] =  self

    def __del__(self):
        try:
          del platformtools.controllers[threading.current_thread().name]
        except:
          pass
            
    def run(self, path):
        pass

    def match(self, path):
        if self.pattern.findall(path):
          return True
        else:
          return False



class Platformtools(object):

  def dialog_ok(self, heading, line1, line2="", line3=""):
    pass

  def dialog_notification(self, heading, message, icon=0, time=5000, sound=True):
    pass

  def dialog_yesno(self, heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
    return True
    
  def dialog_select(self, heading, list): 
    pass
    
  def dialog_progress(self, heading, line1, line2="", line3=""):
    class Dialog(object):
        def __init__(self, heading, line1, line2, line3, PObject):
            self.PObject = PObject
            self.closed = False
            self.heading = heading
            text = line1
            if line2: text += "\n" + line2
            if line3: text += "\n" + line3

        def iscanceled(self):
            return self.closed

        def update(self, percent, line1, line2="", line3=""):
            pass

        def close(self):
            self.closed = True

    return Dialog(heading, line1, line2, line3, None)


  def dialog_progress_bg(self, heading, message=""):
    class Dialog(object):
        def __init__(self, heading, message, PObject):
            self.PObject = PObject
            self.closed = False
            self.heading = heading

        def isFinished(self):
            return not self.closed

        def update(self, percent=0, heading="", message=""):
            pass

        def close(self):
            self.closed = True
    return Dialog(heading, message, None)

  def dialog_input(self, default="", heading="", hidden=False):
    return default

  def dialog_numeric(self, type, heading, default=""):
    return None

  def itemlist_refresh(self):
    pass

  def itemlist_update(self, item):
    pass

  def render_items(self, itemlist, parentitem):
    pass

  def is_playing(self):
    return False

  def play_video(self, item):
    pass
 
  def show_channel_settings(self, list_controls=None, dict_values=None, caption="", callback=None, item=None):
    pass
