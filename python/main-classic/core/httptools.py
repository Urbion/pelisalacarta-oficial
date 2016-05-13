# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# httptools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import gzip
import os
import time
import urllib
import urllib2
import urlparse
from StringIO import StringIO
from core import config
from core import logger


def downloadpage(url, post=None, headers=None, timeout=None, follow_redirects=True, cookies=True, update_headers=True):
    """
    funcion downloadpage():
      Función para descargar una página web pasandole la url, admite los modos GET y POST.
      Parametros:
        url                   #Indica la url de la página a descargar
        post                  #Datos POST para la petición
        headers               #Headers para la petición (puede ser un dict() o un list() indistintamente),
                              #estos se añadiran/modificaran los headers por defecto, a no ser que update_headers = False, que en este caso
                              #sustituiran por completo a los headers por defecto.
        timeout               #Timeout para la petición, por defecto None
        follow_redirects      #Indica si se han de seguir las redirecciones, por defecto True
        cookies               #Indica si se han de usar cookies, por defecto True
        update_headers        #Indica si los headers se añadiran/modificaran a los headers por defecto o si se reemplazaran, por defecto True

      Uso:
          response = downloadpege("http://www.example.com")

          data = response.data                  #Datos de respuesta (si response.error es True, contendra el mensaje del error)
          headers = response.headers            #Diccionario con los headers de respuesta
          response_code = response.code         #Codigo de respuesta (si response.error es True, contendra el código del error)
          response error = response.error       #True si se ha producido un error
          response_time = response.time         #Tiempo usado para descargar la página

        Tambien podemos hacer un uso simplificado:
          data = downloadpege("http://www.example.com").data
          headers = downloadpege("http://www.example.com").headers
          content_type = downloadpege("http://www.example.com").headers.get("content-type")
          etc...
    """
    # Diccionario donde almacenaremos los datos de respuesta
    response = {}

    # Headers por defecto, si no se especifica nada
    request_headers = dict()
    request_headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"
    request_headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    request_headers["Accept-Language"] = "es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"
    request_headers["Accept-Charset"] = "utf-8"
    request_headers["Accept-Encoding"] = "gzip"

    # Headers pasados como parametros
    if headers and update_headers:
        request_headers.update(dict(headers))
    elif headers and not update_headers:
        request_headers = dict(headers)

    # Quote sencillo para codificar caracteres no válidos
    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")

    # Directorio donde se almacenan las cookies
    cookies_path = os.path.join(config.get_data_path(), "cookies")
    if not os.path.exists(cookies_path):
        os.mkdir(cookies_path)

    # Fichero de cookies para dominio
    ficherocookies = os.path.join(cookies_path, urlparse.urlparse(url).hostname + ".dat")

    # Guardamos un resumen de la petición en el log
    logger.info("------------------------------------------")
    logger.info("pelisalacarta.core.httptools  downloadpage")
    logger.info("------------------------------------------")
    logger.info("Timeout: %s" % timeout)
    logger.info("URL: " + url)
    logger.info("Dominio: " + urlparse.urlparse(url).hostname)
    logger.info("Peticion: %s" % ("POST" if post else "GET"))
    logger.info("Usar Cookies: %s" % cookies)
    logger.info("Fichero de Cookies: " + ficherocookies)
    logger.info("Headers:")
    for header in request_headers:
        logger.info("- " + header + ":" + request_headers[header])

    # Handlers usados para la petición
    # HTTPHandler con debuglevel False
    handlers = [urllib2.HTTPHandler(debuglevel=False)]

    # Si no seguimos las redirecciones añadiremos NoRedirectHandler
    if not follow_redirects:
        handlers.append(NoRedirectHandler())

    # Si usamos redirecciones añadiremos HTTPCookieProcessor
    if cookies:
        cj = cookielib.MozillaCookieJar()
        if os.path.isfile(ficherocookies):
            logger.info("Leyendo fichero cookies")
            try:
                cj.load(ficherocookies, ignore_discard=True)
            except:
                logger.info("El fichero de cookies existe pero es ilegible, se borra")
                os.remove(ficherocookies)
        handlers.append(urllib2.HTTPCookieProcessor(cj))

    # Creamos el opener con los handlers seleccionados
    opener = urllib2.build_opener(*handlers)

    # Contador
    inicio = time.time()

    # Iniciamos la petición
    logger.info("Realizando Peticion")
    req = urllib2.Request(url, post, request_headers)
    try:
        handle = opener.open(req, timeout=timeout)

    # Capturamos los errores HTTP
    except urllib2.HTTPError, e:
        response["error"] = True
        response["code"] = e.code
        response["headers"] = e.headers.dict
        response["data"] = str(e)
        response["time"] = time.time() - inicio

    # Capturamos el resto de errores
    except Exception, e:
        response["error"] = True
        response["code"] = None
        response["headers"] = dict()
        response["data"] = str(e)
        response["time"] = time.time() - inicio

        # Si no hay error recogemos los datos
    else:
        response["error"] = False
        response["code"] = handle.getcode()
        response["headers"] = handle.headers.dict
        response["data"] = handle.read()
        response["time"] = time.time() - inicio

    # Si el contenido esta comprimido, lo descomprimimos
    if response["headers"].get('content-encoding') == 'gzip':
        logger.info("Descomprimiendo...")
        response["data"] = gzip.GzipFile(fileobj=StringIO(response["data"])).read()
        logger.info("Descomprimido")

    # Guardamos en el log un resumen con la respuesta
    logger.info("Terminado en %.2f segundos" % (response["time"]))
    logger.info("Response error: %s" % (response["error"]))
    logger.info("Response code: %s" % (response["code"]))
    logger.info("Response headers:")
    for header in response["headers"]:
        logger.info("- " + header + ":" + response["headers"][header])

    # Guardamos las cookies
    if cookies:
        logger.info("Guardando cookies...")
        cj.save(ficherocookies, ignore_discard=True)

    return type('Enum', (), response)


class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl

    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
