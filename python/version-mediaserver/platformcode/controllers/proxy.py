# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para acceso indirecto a ficheros remotos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from controller import Controller
from core import config
import os
import re
from core import logger
import time 
import urllib2, urllib
import base64

class proxy(Controller):
    pattern = re.compile("^/proxy/")
    
    def run(self, path):
        url= path.replace("/proxy/","").split("/")[0]
        url = base64.b64decode(urllib.unquote_plus(url))

        Headers = self.handler.headers.dict
        
        h=urllib2.HTTPHandler(debuglevel=0)
        request = urllib2.Request(url)
        request.add_header("Accept-Encoding","")
        
        for header in Headers:
          if not header in ["host","referer"]:
            request.add_header(header,Headers[header])
          
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)  
        connexion = opener.open(request)
        self.handler.send_response(connexion.getcode())
        
        ResponseHeaders = connexion.info()
        logger.info("------------------------------------")
        logger.info(url)
        logger.info(connexion.getcode())
        logger.info("Headers:")
        for header in ResponseHeaders:
            self.handler.send_header(header, ResponseHeaders[header])
            logger.info("Reenviado Header ->" + header + "=" + ResponseHeaders[header])
  
        self.handler.end_headers()
        
        blocksize = 1024
        bloqueleido = connexion.read(blocksize)
        while len(bloqueleido)>0:
          self.handler.wfile.write(bloqueleido)
          bloqueleido = connexion.read(blocksize)
          
        logger.info("Terminado")
        logger.info("------------------------------------")
        
        self.handler.wfile.close()
        connexion.close()