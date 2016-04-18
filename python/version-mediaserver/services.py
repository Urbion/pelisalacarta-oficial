# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC services
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from threading import Thread

def Updater():
  from core import channel_updater
  channel_updater.Check()

#Thread(target=Updater).start() 
