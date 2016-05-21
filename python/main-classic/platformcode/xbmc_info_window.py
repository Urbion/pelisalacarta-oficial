# -*- coding: utf-8 -*-
import xbmcgui
from core.tmdb import Tmdb
from core.item import Item
import re

class InfoWindow(xbmcgui.WindowXMLDialog):
  item_title = ""
  item_serie = ""
  item_temporada = 0
  item_episodio = 0
  result = {}
  
  def get_language(self, lng):
    #Cambiamos el formato del Idioma
    languages = {'aa': 'Afar', 'ab': 'Abkhazian', 'af': 'Afrikaans', 'ak': 'Akan', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'an': 'Aragonese', 'hy': 'Armenian', 'as': 'Assamese', 'av': 'Avaric', 'ae': 'Avestan', 'ay': 'Aymara', 'az': 'Azerbaijani', 'ba': 'Bashkir', 'bm': 'Bambara', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bh': 'Bihari languages', 'bi': 'Bislama', 'bo': 'Tibetan', 'bs': 'Bosnian', 'br': 'Breton', 'bg': 'Bulgarian', 'my': 'Burmese', 'ca': 'Catalan; Valencian', 'cs': 'Czech', 'ch': 'Chamorro', 'ce': 'Chechen', 'zh': 'Chinese', 'cu': 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'cv': 'Chuvash', 'kw': 'Cornish', 'co': 'Corsican', 'cr': 'Cree', 'cy': 'Welsh', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'dv': 'Divehi; Dhivehi; Maldivian', 'nl': 'Dutch; Flemish', 'dz': 'Dzongkha', 'el': 'Greek, Modern (1453-)', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'eu': 'Basque', 'ee': 'Ewe', 'fo': 'Faroese', 'fa': 'Persian', 'fj': 'Fijian', 'fi': 'Finnish', 'fr': 'French', 'fr': 'French', 'fy': 'Western Frisian', 'ff': 'Fulah', 'Ga': 'Georgian', 'de': 'German', 'gd': 'Gaelic; Scottish Gaelic', 'ga': 'Irish', 'gl': 'Galician', 'gv': 'Manx', 'el': 'Greek, Modern (1453-)', 'gn': 'Guarani', 'gu': 'Gujarati', 'ht': 'Haitian; Haitian Creole', 'ha': 'Hausa', 'he': 'Hebrew', 'hz': 'Herero', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'ig': 'Igbo', 'is': 'Icelandic', 'io': 'Ido', 'ii': 'Sichuan Yi; Nuosu', 'iu': 'Inuktitut', 'ie': 'Interlingue; Occidental', 'ia': 'Interlingua (International Auxiliary Language Association)', 'id': 'Indonesian', 'ik': 'Inupiaq', 'is': 'Icelandic', 'it': 'Italian', 'jv': 'Javanese', 'ja': 'Japanese', 'kl': 'Kalaallisut; Greenlandic', 'kn': 'Kannada', 'ks': 'Kashmiri', 'ka': 'Georgian', 'kr': 'Kanuri', 'kk': 'Kazakh', 'km': 'Central Khmer', 'ki': 'Kikuyu; Gikuyu', 'rw': 'Kinyarwanda', 'ky': 'Kirghiz; Kyrgyz', 'kv': 'Komi', 'kg': 'Kongo', 'ko': 'Korean', 'kj': 'Kuanyama; Kwanyama', 'ku': 'Kurdish', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'li': 'Limburgan; Limburger; Limburgish', 'ln': 'Lingala', 'lt': 'Lithuanian', 'lb': 'Luxembourgish; Letzeburgesch', 'lu': 'Luba-Katanga', 'lg': 'Ganda', 'mk': 'Macedonian', 'mh': 'Marshallese', 'ml': 'Malayalam', 'mi': 'Maori', 'mr': 'Marathi', 'ms': 'Malay', 'Mi': 'Micmac', 'mk': 'Macedonian', 'mg': 'Malagasy', 'mt': 'Maltese', 'mn': 'Mongolian', 'mi': 'Maori', 'ms': 'Malay', 'my': 'Burmese', 'na': 'Nauru', 'nv': 'Navajo; Navaho', 'nr': 'Ndebele, South; South Ndebele', 'nd': 'Ndebele, North; North Ndebele', 'ng': 'Ndonga', 'ne': 'Nepali', 'nl': 'Dutch; Flemish', 'nn': 'Norwegian Nynorsk; Nynorsk, Norwegian', 'nb': 'Bokmål, Norwegian; Norwegian Bokmål', 'no': 'Norwegian', 'oc': 'Occitan (post 1500)', 'oj': 'Ojibwa', 'or': 'Oriya', 'om': 'Oromo', 'os': 'Ossetian; Ossetic', 'pa': 'Panjabi; Punjabi', 'fa': 'Persian', 'pi': 'Pali', 'pl': 'Polish', 'pt': 'Portuguese', 'ps': 'Pushto; Pashto', 'qu': 'Quechua', 'rm': 'Romansh', 'ro': 'Romanian; Moldavian; Moldovan', 'ro': 'Romanian; Moldavian; Moldovan', 'rn': 'Rundi', 'ru': 'Russian', 'sg': 'Sango', 'sa': 'Sanskrit', 'si': 'Sinhala; Sinhalese', 'sk': 'Slovak', 'sk': 'Slovak', 'sl': 'Slovenian', 'se': 'Northern Sami', 'sm': 'Samoan', 'sn': 'Shona', 'sd': 'Sindhi', 'so': 'Somali', 'st': 'Sotho, Southern', 'es': 'Spanish', 'sq': 'Albanian', 'sc': 'Sardinian', 'sr': 'Serbian', 'ss': 'Swati', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'ty': 'Tahitian', 'ta': 'Tamil', 'tt': 'Tatar', 'te': 'Telugu', 'tg': 'Tajik', 'tl': 'Tagalog', 'th': 'Thai', 'bo': 'Tibetan', 'ti': 'Tigrinya', 'to': 'Tonga (Tonga Islands)', 'tn': 'Tswana', 'ts': 'Tsonga', 'tk': 'Turkmen', 'tr': 'Turkish', 'tw': 'Twi', 'ug': 'Uighur; Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda', 'vi': 'Vietnamese', 'vo': 'Volapük', 'cy': 'Welsh', 'wa': 'Walloon', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang; Chuang', 'zh': 'Chinese', 'zu': 'Zulu'}
    return languages.get(lng,lng)
    
  def get_date(self, date):
    #Cambiamos el formato de la fecha
    if date:
      return date.split("-")[2] + "/" + date.split("-")[1] + "/" + date.split("-")[0]
    else:
      return "N/A"

  def get_episode_from_title(self, item):
    #Patron para temporada y episodio "1x01"
    pattern = re.compile("([0-9]+)[ ]*[x|X][ ]*([0-9]+)")
    
    #Busca en title
    matches = pattern.findall(item.title)
    if len(matches):
      self.item_temporada = matches[0][0]
      self.item_episodio = matches[0][1]
    
    #Busca en fulltitle  
    matches = pattern.findall(item.fulltitle)
    if len(matches):
      self.item_temporada = matches[0][0]
      self.item_episodio = matches[0][1]
      
    #Busca en contentTitle
    matches = pattern.findall(item.contentTitle)
    if len(matches):
      self.item_temporada = matches[0][0]
      self.item_episodio = matches[0][1]
    
  
  
  def get_item_info(self, item):
  
    #Recogemos los parametros del Item que nos interesan:  
    if "title" in item and item.title !="":
      self.item_title = item.title  
    if "fulltitle" in item and item.fulltitle !="":
      self.item_title = item.fulltitle    
    if "contentTitle" in item and item.contentTitle !="":
      self.item_title = item.contentTitle
    
    
    if "show" in item and item.show !="":
      self.item_serie = item.show  
    if "contentSerieName" in item and item.contentSerieName !="":
      self.item_serie = item.contentSerieName
      
    if "contentSeason" in item and item.contentSeason !="":
      self.item_temporada = item.contentSeason
    if "contentepisodeNumber" in item and item.contentepisodeNumber !="":
      self.item_episodio = item.contentepisodeNumber

    #Si no existen contentepisodeNumber o contentSeason intenta sacarlo del titulo
    if not self.item_episodio or not self.item_temporada:
      self.get_episode_from_title(item)
      
  def get_dict_info(self,dct):
    self.result = dct
    
  def get_tmdb_movie_data(self, text):
      #Buscamos la pelicula
      movie_info = Tmdb(texto_buscado=text, idioma_busqueda="es", tipo="movie")
      
      #Si no hay resultados salimos
      if not len(movie_info.results):
        return False
      
      #Obtenemos la id de la pelicula, y solizitamos los datos de esa pelicula  
      id = movie_info.get_id()
      movie_info = Tmdb(id_Tmdb=id, idioma_busqueda="es", tipo="movie")
      
      #Si no hay resultados salimos
      if not len(movie_info.results):
        return False
      
      #Informacion de la pelicula  
      self.result["type"] = "movie"
      self.result["title"] = movie_info.result["title"] 
      self.result["original_title"] = movie_info.result["original_title"]
      self.result["date"]  = self.get_date(movie_info.result["release_date"])
      self.result["language"]  = self.get_language(movie_info.result["original_language"])
      self.result["rating"]  = movie_info.result["vote_average"] + "/10 (" + movie_info.result["vote_count"] + ")"
      self.result["genres"]  = ", ".join(movie_info.result["genres"])
      self.result["thumbnail"]  = movie_info.get_poster()
      self.result["fanart"] = movie_info.get_backdrop()
      self.result["overview"] = movie_info.result["overview"]
      
      return True

  def get_tmdb_tv_data(self, text, season=0, episode=0):
      #Pasamos la temporada y episodeo a int()
      season = int(season)
      episode=int(episode)
      
      #Buscamos la serie
      serie_info = Tmdb(texto_buscado=text, idioma_busqueda="es", tipo="tv")
      
      #Si no hay resultados salimos
      if not len(serie_info.results):
        return False
      
      #Obtenemos la id de la serie, y solizitamos los datos de esa serie  
      id = serie_info.get_id()
      serie_info = Tmdb(id_Tmdb=id, idioma_busqueda="es", tipo="tv")
      
      
      #informacion generica de la serie
      self.result["type"] = "tv"
      self.result["title"] = serie_info.result.get("name","N/A")
      self.result["rating"] = serie_info.result["vote_average"] + "/10 (" + serie_info.result["vote_count"] + ")"
      self.result["genres"] = ", ".join(serie_info.result["genres"])
      self.result["language"] = self.get_language(serie_info.result["original_language"])
      self.result["thumbnail"] = serie_info.get_poster()
      self.result["fanart"] = serie_info.get_backdrop()
      self.result["overview"] = serie_info.result.get("overview","N/A")
      self.result["seasons"] = str(serie_info.result.get("number_of_seasons",0))
         
      
      #Si tenemos informacion de temporada y episodio      
      if season and episode:
        if season > self.result["seasons"]: season = self.result["season_count"]
        if episode > serie_info.result.get("seasons")[season-1]["episode_count"]: episode = serie_info.result.get("seasons")[season]["episode_count"]
        
        #Solicitamos información del episodio concreto
        season_info = serie_info.get_episodio(season,episode)
        
        #informacion de la temporada
        self.result["season"] = str(season)
        if season_info.get("temporada_poster"): self.result["thumbnail"] = season_info.get("temporada_poster") 
        if serie_info.result.get("overview"): self.result["overview"] =  serie_info.result.get("overview")
        
        #informacion del episodeo
        self.result["episode"] = str(episode)
        self.result["episodes"] = str(len(serie_info.temporada["episodes"]))
        self.result["episode_title"] = serie_info.temporada["episodes"][episode -1].get("name","N/A") 
        self.result["date"] = self.get_date(serie_info.temporada["episodes"][episode -1].get("air_date"))
        if season_info.get("episodio_imagen"): self.result["fanart"] = season_info.get("episodio_imagen")
        if serie_info.temporada["episodes"][episode -1].get("overview"): self.result["overview"] = serie_info.temporada["episodes"][episode -1].get("overview")
        
      return True
 
  def Start(self, data, heading="Información del vídeo"):
    self.heading =  heading
    
    if type(data) == Item:
      self.from_tmdb = True
      self.get_item_info(data)

      #Modo Pelicula
      if not self.item_serie:
        encontrado = self.get_tmdb_movie_data(self.item_title)
        if not encontrado:
          encontrado = self.get_tmdb_tv_data(self.item_title, self.item_temporada, self.item_episodio)

           
      else:
        encontrado = self.get_tmdb_tv_data(self.item_serie, self.item_temporada, self.item_episodio)
        if not encontrado:
          encontrado = self.get_tmdb_movie_data(self.item_serie)

    if type(data) == dict:
      self.from_tmdb = False
      self.get_dict_info(data)
      
    self.doModal()
    
  def onInit(self):
      #Ponemos el foco en el boton de cerrar [X]
      self.setFocus(self.getControl(10003))
      
      #Ponemos el título y las imagenes
      self.getControl(10002).setLabel(self.heading)
      self.getControl(10004).setImage(self.result.get("fanart",""))
      self.getControl(10005).setImage(self.result.get("thumbnail","InfoWindow/img_no_disponible.png"))
      
      #Cargamos los datos para el formato pelicula
      if self.result.get("type","movie") == "movie":
        self.getControl(10006).setLabel("Titulo:")
        self.getControl(10007).setLabel(self.result.get("title","N/A"))
        self.getControl(10008).setLabel("Titulo Original:")
        self.getControl(10009).setLabel(self.result.get("original_title","N/A"))
        self.getControl(100010).setLabel("Idioma original:")
        self.getControl(100011).setLabel(self.result.get("language","N/A"))
        self.getControl(100012).setLabel("Puntuacion:")
        self.getControl(100013).setLabel(self.result.get("rating","N/A"))
        self.getControl(100014).setLabel("Lanzamiento:")
        self.getControl(100015).setLabel(self.result.get("date","N/A"))
        self.getControl(100016).setLabel("Generos:")
        self.getControl(100017).setLabel(self.result.get("genres","N/A"))
        
        #Sinopsis
        self.getControl(100022).setLabel("Sinopsis:")
        self.getControl(100023).setText(self.result.get("overview","N/A"))
      
      #Cargamos los datos para el formato pelicula  
      else:
        self.getControl(10006).setLabel("Serie:")
        self.getControl(10007).setLabel(self.result.get("title","N/A"))
        self.getControl(10008).setLabel("Titulo:")
        self.getControl(10009).setLabel(self.result.get("episode_title","N/A"))
        self.getControl(100010).setLabel("Temporada:")
        self.getControl(100011).setLabel(self.result.get("season","N/A") + " de " + self.result.get("seasons","N/A"))
        self.getControl(100012).setLabel("Episodio:")
        self.getControl(100013).setLabel(self.result.get("episode","N/A") + " de " + self.result.get("episodes","N/A"))
        self.getControl(100014).setLabel("Idioma original:")
        self.getControl(100015).setLabel(self.result.get("language","N/A"))
        self.getControl(100016).setLabel("Puntuacion:")
        self.getControl(100017).setLabel(self.result.get("rating","N/A"))
        self.getControl(100018).setLabel("Emision:")
        self.getControl(100019).setLabel(self.result.get("date","N/A"))
        self.getControl(100020).setLabel("Generos:")
        self.getControl(100021).setLabel(self.result.get("genres","N/A"))
        
        #Sinopsis
        self.getControl(100022).setLabel("Sinopsis:")
        self.getControl(100023).setText(self.result.get("overview","N/A"))
        
  def onClick(self, id):
        #Boton cerrar [X]
        if id == 10003:
            self.close()

  def onAction(self, action):
        if self.from_tmdb:
          #Accion 1: Flecha izquierda
          if action == 1:
            if self.result.get("type","movie") == "tv":
              if self.result.get("title") and self.result.get("season") and self.result.get("episode") and int(self.result.get("episode")) > 1:
                self.get_tmdb_tv_data(self.result.get("title"), season=self.result.get("season"), episode=int(self.result.get("episode"))-1)
                self.onInit()
                
          #Accion 2: Flecha derecha
          if action == 2:
            if self.result.get("type","movie") == "tv":
              if self.result.get("title") and self.result.get("season") and self.result.get("episode") and int(self.result.get("episode")) < int(self.result.get("episodes")):
                self.get_tmdb_tv_data(self.result.get("title"), season=self.result.get("season"), episode=int(self.result.get("episode"))+1)
                self.onInit()

          #Accion 3: Flecha arriba
          if action == 3:
            if self.result.get("type","movie") == "tv":
              if self.result.get("title") and self.result.get("season") and self.result.get("episode") and int(self.result.get("season")) < int(self.result.get("seasons")):
                self.get_tmdb_tv_data(self.result.get("title"), season=int(self.result.get("season"))+1, episode=self.result.get("episode"))
                self.onInit()

          #Accion 4: Flecha abajo
          if action == 4:
            if self.result.get("type","movie") == "tv":
              if self.result.get("title") and self.result.get("season") and self.result.get("episode") and int(self.result.get("season")) >1 :
                self.get_tmdb_tv_data(self.result.get("title"), season=int(self.result.get("season"))-1, episode=self.result.get("episode"))
                self.onInit()