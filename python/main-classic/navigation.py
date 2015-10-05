# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# Generic Launcher
# http://blog.tvalacarta.info/plugin-xbmc/
#------------------------------------------------------------

import os
import sys
from core.item import Item
from core import logger
from core import config
from core import guitools

def NextItem(item):
    PrintItems(item)
    
    itemlist = []
    if item.channel: channelmodule = ImportarCanal(item.channel)
    else: return []
    
    if item.action=="play":
      itemlist = ActionPlay(channelmodule, item)
             
    elif item.action=="findvideos":
      itemlist = ActionFindvideos(channelmodule, item)
    elif item.action=="search":
      itemlist = ActionSearch(channelmodule, item)
    else:
      #Si existe la funcion en el canal la ejecuta
      if hasattr(channelmodule, item.action):
        logger.info("Ejectuando accion: " + item.channel + "." + item.action + "(item)")
        exec "itemlist = channelmodule." + item.action + "(item)"
        
      #Si existe la funcion en el launcher la ejecuta
      elif hasattr(sys.modules[__name__], item.action):
        logger.info("Ejectuando accion: " + item.action + "(item)")
        exec "itemlist =" + item.action + "(item)"
        
      #Si no existe devuelve un error
      else:
          logger.info("No se ha encontrado la accion ["+ item.action + "] en el canal ["+item.channel+"] ni en el launcher")
                  
    if type(itemlist)==list:
      if  len(itemlist) ==0:
        itemlist = [ Item(title="No hay elementos para mostrar", thumbnail=os.path.join(config.get_runtime_path() , "resources" , "images" , "thumb_error.png" )) ]

      itemlist = PostItem(item,itemlist)
    
      PrintItems(itemlist)
      
    return itemlist

#ACCIONES------------------------------------------------------
def ActionPlay(channelmodule,item):
  logger.info("ACCION PLAY")
  if hasattr(channelmodule, 'play'):
    logger.info("Ejecutando funcion play del canal")
    video_items = channelmodule.play(item)
    play(video_items[0])
  else:
    logger.info("Ejecutando funcion play generica")
    play(item)
  return None
  
def ActionFindvideos(channelmodule,item):
  logger.info("ACCION FINDVIDEOS")
  if hasattr(channelmodule, 'findvideos'):
    itemlist = channelmodule.findvideos(item)
  else:
    itemlist = findvideos(item)
  return itemlist
    
def ActionSearch(channelmodule,item):
  logger.info("ACCION SEARCH")
  tecleado = guitools.Keyboard("")
  if (tecleado):
    itemlist = channelmodule.search(item,tecleado)
  else:
    itemlist = []
  return itemlist

#------------------------------------------------------------   
def ItemInfo(parent, item, windowmode):
    item.title = unicode(item.title,"utf-8","ignore").encode("utf8")
    item.fulltitle = unicode(item.fulltitle,"utf-8","ignore").encode("utf8")
    item.plot = unicode(item.plot,"utf-8","ignore").encode("utf8")
    titulo = item.title
    
    import time   
    if item.duration:
      if item.duration > 3599: 
        Tiempo = time.strftime("%H:%M:%S", time.gmtime(item.duration))
      else:
        Tiempo= time.strftime("%M:%S", time.gmtime(item.duration))
    if item.action <> "mainlist":
      if config.get_setting("duracionentitulo")=="true" and item.duration: titulo = titulo + " [COLOR gold](" + Tiempo + ")[/COLOR]" 
      if config.get_setting("calidadentitulo")=="true" and item.quality: titulo = titulo + " [COLOR orange][" + item.quality + "][/COLOR]"   
      if config.get_setting("idiomaentitulo")=="true" and item.language: titulo = titulo + " [COLOR green][" + item.language + "][/COLOR]"
      
    #Si el item tiene fulltitle este manda sobre lo anterior, se mostrara este. 
    if item.fulltitle:
      titulo=item.fulltitle
    thumbnail = item.thumbnail
    if thumbnail == "" and item.folder == True: thumbnail = "%s/thumb_folder.png"
    if thumbnail == "" and item.folder == False: thumbnail = "%s/thumb_nofolder.png"

    if windowmode == 2:
      if "%sthumb_atras.png" in thumbnail: thumbnail = thumbnail %(os.path.join(config.get_runtime_path(), 'resources', "images","icon_"))
      if "%s" in thumbnail: thumbnail = thumbnail %(config.get_thumbnail_path(""))
    else:
      if "%sthumb_atras.png" in thumbnail: thumbnail = thumbnail %(os.path.join(config.get_runtime_path(), 'resources', "images",""))
      if "%s" in thumbnail: thumbnail = thumbnail %(config.get_thumbnail_path("bannermenu"))
    
    return item, titulo, thumbnail


def PostItem(item, itemlist):
    for x in range(len(itemlist)):
    
      #Menu Contextual "Favoritos"
      if itemlist[x].context:
          context = itemlist[x].context.split("|")
      else:
          context=[]
          
          
      if not item.channel in ["channelselector","favoritos","buscador","descargas","biblioteca", "novedades"] or item.channel =="channelselector" and item.action =="listchannels":
        context.append("Añadir a Favoritos,add_to_favorites")
      if itemlist[x].action == "play" and not itemlist[x].channel =="descargas":
        context.append("Descargar,download")
        
        
        
      itemlist[x].context= "|".join(context) 
        
      #Icono Search
      if itemlist[x].thumbnail =="" and itemlist[x].action =="search":
        itemlist[x].thumbnail="%s/search.png"
        
      if itemlist[x].fanart=="":
        channel_fanart = os.path.join( config.get_runtime_path(), 'resources', 'images', 'fanart', itemlist[x].channel+'.jpg')
        if os.path.exists(channel_fanart):
            itemlist[x].fanart = channel_fanart
        else:
            itemlist[x].fanart = os.path.join(config.get_runtime_path(),"fanart.jpg")
    return itemlist


def PrintItems(itemlist):
  if type(itemlist)==list:
    if len(itemlist) >0:
      logger.info("Items devueltos")  
      logger.info("-----------------------------------------------------------------------")
      for item in itemlist:
        logger.info(item.tostring())
      logger.info("-----------------------------------------------------------------------")
  else:
    item =  itemlist
    logger.info("-----------------------------------------------------------------------")
    logger.info("Canal=" + item.channel + " Acción=" + item.action)    
    logger.info("-----------------------------------------------------------------------")
    
    
def ImportarCanal(channel):
  channelmodule=""
  if os.path.exists(os.path.join( config.get_runtime_path(), "channels",channel+".py")):
    exec "from channels import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),"core",channel+".py")):
    exec "from core import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),channel+".py")):
    exec "import "+channel+" as channelmodule"
  return channelmodule


def findvideos(item):
    logger.info("findvideos")
    itemlist = []
    from core import scrapertools
    from servers import servertools
    from servers import longurl
    import copy
    data = scrapertools.cache_page(item.url)
    data=longurl.get_long_urls(data)  
    listavideos = servertools.findvideos(data)  
    for video in listavideos:
        NuevoItem = copy.deepcopy(item)
        NuevoItem.title = item.title
        NuevoItem.fulltitle = "Ver en: ["  + video[2] + "]"
        NuevoItem.url = video[1]
        NuevoItem.server = video[2]
        NuevoItem.action = "play"
        NuevoItem.folder=False
        itemlist.append(NuevoItem)
        
    return itemlist


def play(item):
  opciones = MenuVideo(item)
  if len(opciones) >0:
    opcion = MostrarMenuVideo(item,opciones)
    if not opcion == None:
      exec opciones[opcion].action+"(item, opciones[opcion])"
    else:
      play_video(item,None)
      

def MenuVideo(item):
    if item.server=="": item.server="directo" 
    default_action = config.get_setting("default_action")
    itemlist = []
    
    # Extrae las URL de los vídeos, y si no puedes verlo te dice el motivo
    from servers import servertools
    video_urls,puedes,motivo = servertools.resolve_video_urls_for_playing(item.server,item.url,item.password, True)
 
    
    # Si puedes ver el vídeo, presenta las opciones
    if puedes:
      for video_url in video_urls:
        itemlist.append(Item(title=config.get_localized_string(30151) + " " + video_url[0], url=video_url, action="play_video"))
        
      if item.server=="local":
        itemlist.append(Item(title=config.get_localized_string(30164), url=video_urls, action="delete"))

      if not item.server=="local":
        itemlist.append(Item(title=config.get_localized_string(30153), url=video_urls, action="download")) #"Descargar"

      if item.channel=="favoritos":
        itemlist.append(Item(title=config.get_localized_string(30154), url=video_urls, action="remove_from_favorites")) #"Quitar de favoritos"
      
      if not item.channel=="favoritos":
        itemlist.append(Item(title=config.get_localized_string(30155), url=video_urls, action="add_to_favorites"))  #"Añadir a favoritos"
      
      if not item.channel=="library":
        itemlist.append(Item(title=config.get_localized_string(30161), url=video_urls, action="add_to_library")) #"Añadir a Biblioteca"
        
      if item.channel=="library":
        itemlist.append(Item(title="Quitar de la Biblioteca", url=video_urls, action="remove_from_library")) #"Añadir a Biblioteca"

      if not item.channel=="descargas":
        itemlist.append(Item(title=config.get_localized_string(30157), url=video_urls, action="add_to_downloads")) #"Añadir a lista de descargas"
            
      if item.channel =="descargas" and item.category=="errores":
        itemlist.append(Item(title=config.get_localized_string(30159), url=video_urls, action="remove_from_error_downloads")) #"Borrar descarga definitivamente"
        itemlist.append(Item(title=config.get_localized_string(30160), url=video_urls, action="add_again_to_downloads")) #"Pasar de nuevo a lista de descargas"   
               
      if item.channel =="descargas" and item.category=="pendientes": 
        itemlist.append(Item(title=config.get_localized_string(30156), url=video_urls, action="remove_from_downloads")) #"Quitar de lista de descargas"

      if config.get_setting("jdownloader_enabled")=="true": 
        itemlist.append(Item(title=config.get_localized_string(30158), url=video_urls, action="send_to_jdownloader")) #"Enviar a JDownloader"
          
      if config.get_setting("pyload_enabled")=="true": 
        itemlist.append(Item(title=config.get_localized_string(30158).replace("jDownloader","pyLoad"), url=video_urls, action="send_to_pyLoad")) #"Enviar a pyLoad"

      if not item.channel in ["trailertools","ecarteleratrailers"]: 
        itemlist.append(Item(title=config.get_localized_string(30162), url=video_urls, action="search_trailer")) # "Buscar Trailer" 
        
    else:
        if item.server!="":
          guitools.Dialog_OK( "No puedes ver ese vídeo porque..." , motivo.replace("<br/>","\n") + "\n" + item.url)

        else:
            guitools.Dialog_OK("No puedes ver ese vídeo porque...","El servidor donde está alojado no está\nsoportado en pelisalacarta todavía\n"+url)

            if item.channel=="favoritos":
              itemlist.append(Item(title=config.get_localized_string(30154), url=video_urls, action="remove_from_favorites")) #"Quitar de favoritos"
            if item.channel=="library":
              itemlist.append(Item(title="Quitar de la Biblioteca", url=video_urls, action="remove_from_library")) #"Añadir a Biblioteca"

            if item.channel =="descargas" and item.category=="errores":
              itemlist.append(Item(title=config.get_localized_string(30159), url=video_urls, action="remove_from_error_downloads")) #"Borrar descarga definitivamente"         
            if item.channel =="descargas" and not item.category=="errores": 
              itemlist.append(Item(title=config.get_localized_string(30156), url=video_urls, action="remove_from_downloads")) #"Quitar de lista de descargas"

    return itemlist


#Función encargada de Mostrar el Menú de Reproduccion y devolver la opción seleccionada:----------->OK
def MostrarMenuVideo(item,itemlist):
    opciones = []
    Reproducible = False
    seleccion = -1
    for itemopcion in itemlist:
      opciones.append(itemopcion.title)
      if itemopcion.action=="play": Reproducible = True

    if len(opciones)>0:    
      default_action = config.get_setting("default_action")
      if default_action=="0" or not Reproducible: #Preguntar
        seleccion =guitools.Dialog_Select(config.get_localized_string(30163), opciones)
      elif default_action=="1": #Ver en Calidad Baja
          seleccion = 0
      elif default_action=="2": #Ver en Calidad Alta
          seleccion = len(video_urls)-1
      elif default_action=="3": #Mandar a jDownloader
        if config.get_setting("jdownloader_enabled")=="true":
          seleccion = opciones.index(OpcionesDisponibles[10])
      else:
          seleccion=0
    return seleccion
    
#Función encargada de reproducir un vídeo:----------->OK
def play_video(item, VideoItem = None):
  if item.server == "torrent":
    if VideoItem is not None:
      from core import torrent_player
      torrent_player.download(item, VideoItem, True)
  else:
    guitools.play(item, VideoItem)
    
#-------------------------------------
#-------------------------------------
#-------------------------------------
#-------------------------------------

def add_to_favorites(item, VideoItem = None):
  from core import favoritos
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.fulltitle=""
    favoritos.GuardarFavorito(item)
    guitools.Dialog_OK(config.get_localized_string(30102) , item.title + "\n" + config.get_localized_string(30108)) # 'se ha añadido a favoritos'

#Función para eliminar un vídeo de Favoritos:----------->OK
def remove_from_favorites(item, VideoItem = None): 
  from core import favoritos
  favoritos.BorrarFavorito(item)

  guitools.Dialog_OK(config.get_localized_string(30102) , item.title + "\n" + config.get_localized_string(30105)) # 'Se ha quitado de favoritos'
  guitools.Refresh()
  
def download_all_episodes(item):
    from servers import servertools
    from core import downloadtools
    from core import scrapertools

    # Esto es poco elegante...
    # Esta marca es porque el item tiene algo más aparte en el atributo "extra"
    if item.extra: action = item.extra
    if item.refered_action: action = item.refered_action
    if "###" in action:
      item.extra = action.split("###")[1]
      action = action.split("###")[0]    
        
    #Importamos el canal    
    channel = ImportarCanal(item.channel)
    
    #Ejecutamos la funcion
    exec "itemlist = channel."+action+"(item)"
    
    #Quitamos estos dos elementos de la lista (si los hay)
    for episodio in itemlist:
      if episodio.action=="add_serie_to_library" or episodio.action=="download_all_episodes":
        itemlist.remove(episodio)
    

    #Abrimos el dialogo
    pDialog = guitools.Dialog_Progress('pelisalacarta', 'Descargando ' + item.show)
    
    for x, episodio in enumerate(itemlist):
    
      #Si se presiona cancelar, se cancela
      if pDialog.iscanceled():
        return
      #Extraemos la Temporada y el Episodio  
      episodio.title = scrapertools.get_season_and_episode(episodio.title)
      
      #Actualizamos el progreso
      pDialog.Actualizar(((x)*100)/len(itemlist), 'Descargando ' + item.show, 'Descargando episodio: ' + episodio.title)

      # Extrae los mirrors
      if hasattr(channel, 'findvideos'):
          mirrors_itemlist = channel.findvideos(episodio)
      else:
          mirrors_itemlist = findvideos(episodio,episodio.channel)
      
      
      descargado = False
      
      #Descarga el primer mirror que funcione
      for mirror_item in mirrors_itemlist:
      
        if hasattr(channel, 'play'):
            video_items = channel.play(mirror_item)
        else:
            video_items = [mirror_item]
            
        if len(video_items)>0:
            video_item = video_items[0]
            
            # Comprueba que esté disponible
            video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing( video_item.server , video_item.url , video_password="" , muestra_dialogo=False)
            
            # Lo descarga
            if puedes:
            
              # El vídeo de más calidad es el último
              devuelve = downloadtools.downloadbest(video_urls,item.show+" "+episodio.title+" ["+video_item.server+"]",continuar=False)
              if devuelve==0:
                  logger.info("[launcher.py] download_all_episodes - Archivo Descargado")
                  descargado = True
                  break
              elif devuelve==-1:
                  pDialog.Cerrar()
                  logger.info("[launcher.py] download_all_episodes - Descarga abortada")
                  guitools.Dialog_OK("pelisalacarta" , "La descarga ha sido cancelada")
                  return
              else:
                  continue
    pDialog.Cerrar()

#Función para descargar un vídeo:----------->OK
def download(item, VideoItem = None): 
  from core import descargas
  item.title = guitools.Keyboard(item.title)
  if item.title:
    devuelve = descargas.download(item)
    if devuelve==0: guitools.Dialog_OK("pelisalacarta" , "Descargado con éxito")
    elif devuelve==-1: guitools.Dialog_OK("pelisalacarta" , "Descarga cancelada")
    else: guitools.Dialog_OK("pelisalacarta" , "Error en la descarga")

#Función para añadir un vídeo a la Librería:----------->OK
def add_to_library(item, VideoItem = None): 
  from core import library
  item.title = guitools.Keyboard(item.title)
  if item.title:
    library.Guardar(item)
    guitools.Dialog_OK(config.get_localized_string(30101) , item.title +"\n"+ config.get_localized_string(30135)) # 'Se ha añadido a la Biblioteca'
    library.ActualizarBiblioteca(item) 


#Función para borrar un vídeo de la Librería:----------->OK
def remove_from_library(item, VideoItem = None): 
    from core import library
    library.Borrar(item)
    library.ActualizarBiblioteca(item)    
    
    
#Función para añadir un vídeo a la Lista de Descargas:----------->OK
def add_to_downloads(item, VideoItem = None): 
  from core import descargas
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.fulltitle=""
    descargas.GuardarDescarga(item)
    guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30109)) # 'se ha añadido a la lista de descargas'


#Función para envíar un vídeo a jDownloader:----------->OK pendiente añadir user y password a la config
def send_to_jdownloader(item, VideoItem = None): 
    from core import scrapertools
    import urllib
    import base64
    User=config.get_setting("jdownloader_user")
    Password=config.get_setting("jdownloader_password")
    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
    headers.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
    headers.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
    headers.append(["Accept-Encoding","gzip, deflate"])
    headers.append(["Authorization","Basic " + base64.b64encode(User + ":" + Password)])
    headers.append(["Content-Type","application/x-www-form-urlencoded"])
    url=config.get_setting("jdownloader")+"/link_adder.tmpl"
    Descargas = VideoItem.url[0][1]
    logger.info(Descargas)
    if item.thumbnail: Descargas = Descargas + "\n" + item.thumbnail
    if item.subtitle: Descargas = Descargas + "\n" + item.subtitle
    try:
      data = scrapertools.downloadpage(url,headers=headers,post="do=Add&addlinks="+ urllib.quote_plus(Descargas))
      guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "Se ha enviado a jDownloader")
    except:
      guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "No se ha podido enviar a jDownloader")
    
    

#Función para envíar un vídeo a pyLoad:----------->OK
def send_to_pyLoad(item, VideoItem = None):    
  logger.info("Opcion seleccionada: Enviar a pyLoad" )
  if item.show!="":
      package_name = item.show
  else:
      package_name = item.title
  from core import pyload_client
  pyload_client.download(url=VideoItem.url[0][1],package_name=package_name)
  if item.thumbnail: pyload_client.download(url=item.thumbnail,package_name=package_name)
  if item.subtitle: pyload_client.download(url=item.subtitle,package_name=package_name)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + "Se ha enviado a pyLoad")



#Función para buscar un Trailer:----------->OK
def search_trailer(item, VideoItem = None): 
  logger.info("Opcion seleccionada: Buscar Trailer" )
  item.title = guitools.Keyboard(item.title)
  if item.title:
    item.channel="trailertools"
    item.action="buscartrailer"
    guitools.Update(item)

#Función para eliminar un vídeo de la Lista de Descargas:----------->OK
def remove_from_downloads(item, VideoItem = None):
  from core import descargas
  # La categoría es el nombre del fichero en la lista de descargas
  descargas.BorrarDescarga(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30106)) # 'Se ha quitado de lista de descargas'
  guitools.Refresh()


#Función para eliminar un vídeo de Descargas con error:----------->OK
def remove_from_error_downloads(item, VideoItem = None): 
  from core import descargas
  descargas.delete_error_bookmark(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30106)) # 'Se ha quitado de la lista'
  guitools.Refresh()


#Función para añadir de nuevo un vídeo a Descargas desde Descargas con error:----------->OK
def add_again_to_downloads(item, VideoItem = None): 
  from core import descargas
  descargas.mover_descarga_error_a_pendiente(item)
  guitools.Dialog_OK(config.get_localized_string(30101) , item.title + "\n" + config.get_localized_string(30107)) # 'Ha pasado de nuevo a la lista de descargas'
  guitools.Refresh()
