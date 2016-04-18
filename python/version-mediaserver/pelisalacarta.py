#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import os, sys, socket
sys.dont_write_bytecode = True
from core import logger
from core import config
import threading
from platformcode import platformtools
from functools import wraps
import time
sys.path.append(os.path.join(config.get_runtime_path(), 'lib'))
http_port = int(config.get_setting("server.port"))
websocket_port = int(config.get_setting("websocket.port"))
myip = config.get_local_ip()
platformtools.requests = {}

def ThreadNameWrap(func):
    @wraps(func)
    def bar(*args, **kw):
        if not "name" in kw:
            kw['name'] = threading.current_thread().name
        return func(*args, **kw)

    return bar

threading.Thread.__init__ = ThreadNameWrap(threading.Thread.__init__)


def MostrarInfo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("--------------------------------------------------------------------")
    print ("Pelisalacarta Iniciado")
    print ("La URL para acceder es http://" + myip + ":" + str(http_port))
    print ("WebSocket Server iniciado en ws://" + myip + ":" + str(websocket_port))
    print ("--------------------------------------------------------------------")
    print ("Runtime Path      : " + config.get_runtime_path())
    print ("Data Path         : " + config.get_data_path())
    print ("Download Path     : " + config.get_setting("downloadpath"))
    print ("DownloadList Path : " + config.get_setting("downloadlistpath"))
    print ("Bookmark Path     : " + config.get_setting("bookmarkpath"))
    print ("Library Path      : " + config.get_setting("library_path"))
    print ("--------------------------------------------------------------------")
    conexiones = []
    requests = platformtools.requests
    for a in requests:
        conexiones.append(requests[a].client_ip + " (" + requests[a].name + ")")
    if len(conexiones) > 0:
        print ("Clientes conectados:")
        for conexion in conexiones:
            print (conexion)
    else:
        print ("No hay conexiones")


def start():
    logger.info("pelisalacarta server init...")
    import services
    config.verify_directories_created()
    try:
        import HTTPServer
        HTTPServer.start(MostrarInfo)
        import WebSocket
        WebSocket.start(MostrarInfo)

        # Da por levantado el servicio
        logger.info("--------------------------------------------------------------------")
        logger.info("Pelisalacarta Iniciado")
        logger.info("La URL para acceder es http://" + myip + ":" + str(http_port))
        logger.info("WebSocket Server iniciado en ws://" + myip + ":" + str(websocket_port))
        logger.info("--------------------------------------------------------------------")
        logger.info("Runtime Path      : " + config.get_runtime_path())
        logger.info("Data Path         : " + config.get_data_path())
        logger.info("Download Path     : " + config.get_setting("downloadpath"))
        logger.info("DownloadList Path : " + config.get_setting("downloadlistpath"))
        logger.info("Bookmark Path     : " + config.get_setting("bookmarkpath"))
        logger.info("Library Path      : " + config.get_setting("librarypath"))
        logger.info("--------------------------------------------------------------------")
        MostrarInfo()

        start = True
        while start:
            time.sleep(1)

    except KeyboardInterrupt:
        print 'Deteniendo el servidor HTTP...'
        HTTPServer.stop()
        print 'Deteniendo el servidor WebSocket...'
        WebSocket.stop()
        print 'Pelisalacarta Detenido'
        start = False


# Inicia pelisalacarta
start()
