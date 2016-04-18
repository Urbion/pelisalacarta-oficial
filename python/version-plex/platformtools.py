# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# platformtools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Herramientas responsables de adaptar los diferentes 
# cuadros de dialogo a una plataforma en concreto,
# en este caso Plex.
# version 1.3
# ------------------------------------------------------------
import os
import sys
from core import config
from core import logger

def dialog_ok(heading, line1, line2="", line3=""):
    pass
    
def dialog_notification(heading, message, icon=0, time=5000, sound=True):
    pass

def dialog_yesno(heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
    return True
    
def dialog_select(heading, list): 
    return 0
    
def dialog_progress(heading, line1, line2="", line3=""):
    class Dialog(object):
        def __init__(self, heading, line1, line2, line3, PObject):
            self.PObject = PObject
            self.closed = False
            self.heading = heading

        def iscanceled(self):
            return False

        def update(self, percent, line1, line2="", line3=""):
            pass

        def close(self):
            self.closed = True
    return Dialog(heading, line1, line2, line3, None)


def dialog_progress_bg(heading, message=""):
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

def dialog_input(default="", heading="", hidden=False):
    return default

def dialog_numeric(type, heading, default=""):
    return None

def itemlist_refresh():
    pass

def itemlist_update(item):
    pass

def render_items(itemlist, parentitem):
    pass

def is_playing():
    return False

def play_video(item):
    pass
 
 