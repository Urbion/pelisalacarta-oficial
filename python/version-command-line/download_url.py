# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Script for downloading files from any server supported on pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#-------------------------------------------------------------------------

import re,urllib,urllib2,sys,os
sys.path.append ("lib")

from core import config
config.set_setting("debug","true")

from core import scrapertools
from core import downloadtools
from core.item import Item
from core import servertools

def download_url(url,titulo,server):

    url = url.replace("\\","")

    print "Analizando enlace "+url

    # Averigua el servidor
    if server=="":
        itemlist = servertools.find_video_items(data=url)
        if len(itemlist)==0:
            print "No se puede identificar el enlace"
            return

        item = itemlist[0]
        print "Es un enlace en "+item.server
    else:
        item = Item()
        item.server = server

    # Obtiene las URL de descarga
    video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing(item.server,url)
    if len(video_urls)==0:
        print "No se ha encontrado nada para descargar"
        return

    # Descarga el de mejor calidad, como hace pelisalacarta
    print "Descargando..."
    print video_urls
    devuelve = downloadtools.downloadbest(video_urls,titulo,continuar=True)

if __name__ == "__main__":
    url = sys.argv[1]
    title = sys.argv[2]

    if len(sys.argv)>=4:
        server = sys.argv[3]
    else:
        server = ""

    if title.startswith("http://") or title.startswith("https://"):
        url = sys.argv[2]
        title = sys.argv[1]

    download_url(url,title,server)

