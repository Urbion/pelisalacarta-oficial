# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para xml
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re,sys,os
from core import logger

def xml2dict(file = None, xmldata = None):
  parse = globals().get(sys._getframe().f_code.co_name)
  
  if xmldata == None and file == None:  raise Exception("No hay nada que convertir!")
  if xmldata == None:
    if not os.path.exists(file): raise Exception("El archivo no existe!")
    xmldata = open(file, "rb").read()

  matches = re.compile("<(?P<tag>[^>]+)>[\n]*[\s]*[\t]*(?P<value>.*?)[\n]*[\s]*[\t]*<\/(?P=tag)\s*>",re.DOTALL).findall(xmldata)
  
  return_dict = {} 
  for tag, value in matches:
    #Si tiene elementos
    if "<" and "</" in value:
      if tag in return_dict:
        if type(return_dict[tag])== list:
          return_dict[tag].append(parse(xmldata=value))
        else:
          return_dict[tag] = [dct[tags[x]]]
          return_dict[tag].append(parse(xmldata=value))
      else:
          return_dict[tag] = parse(xmldata=value)
      
    else:
      if tag in return_dict:
        if type(return_dict[tag])== list:
          return_dict[tag].append(value)
        else:
          return_dict[tag] = [return_dict[tag]]
          return_dict[tag].append(value)
      else:
        return_dict[tag] = value 
  return return_dict
