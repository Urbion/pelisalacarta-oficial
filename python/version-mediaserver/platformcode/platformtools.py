# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# platformtools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Herramientas responsables de adaptar los diferentes 
# cuadros de dialogo a una plataforma en concreto,
# en este caso Mediserver.
# version 1.3
# ------------------------------------------------------------
import os
import sys
from core import config
from core import logger
import threading
controllers = {}


def dialog_ok(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_ok(*args, **kwargs)
    
def dialog_notification(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_notification(*args, **kwargs)

def dialog_yesno(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_yesno(*args, **kwargs)
    
def dialog_select(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_select(*args, **kwargs)

def dialog_progress(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_progress(*args, **kwargs)
 
def dialog_progress_bg(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_progress_bg(*args, **kwargs)

def dialog_input(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_input(*args, **kwargs)
    
def dialog_numeric(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.dialog_numeric(*args, **kwargs)

def itemlist_refresh(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.itemlist_refresh(*args, **kwargs)

def itemlist_update(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.itemlist_update(*args, **kwargs)

def render_items(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.render_items(*args,**kwargs)

def is_playing(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.is_playing(*args, **kwargs)

def play_video(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.play_video(*args, **kwargs)

def open_settings(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.open_settings(*args, **kwargs)

def show_channel_settings(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].platformtools.show_channel_settings(*args, **kwargs)