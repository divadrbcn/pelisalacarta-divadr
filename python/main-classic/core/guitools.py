# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import config
import logger
from core.item import Item

def ExtraerItem():
  itemserializado = sys.argv[2].replace("?","")

  item = Item()
  if itemserializado:
    item.deserialize(itemserializado)
  else:
    item = Item(channel="channelselector", action="mainlist")
  return item



class DialogoProgreso(object):
  Progreso=""
  Titulo=""
  Closed=False
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
    self.Closed = False
  def IsCanceled(self):
    return (self.Progreso.iscanceled() or self.Closed)

  
  def Actualizar(self,Porcentaje, Texto):
    import xbmcgui
    Linea1=" "
    Linea2=" "
    Linea3=" "
    if len(Texto.split("\n"))>0:
      Linea1= Texto.split("\n")[0]
    if len(Texto.split("\n"))>1:
      Linea2= Texto.split("\n")[1]
    if len(Texto.split("\n"))>2:
      Linea3= Texto.split("\n")[2]
    self.Progreso.update(Porcentaje,Linea1,Linea2,Linea3)

  def Cerrar(self):
    import xbmcgui
    self.Progreso.close()
    self.Closed = True



def isPlaying():
  import xbmc
  return xbmc.Player().isPlaying()

    
    
def Dialog_Progress(title, Texto):
  import xbmcgui
  progreso = xbmcgui.DialogProgress()
  progreso.create(title , Texto)
  Progreso = DialogoProgreso(progreso,title)
  return Progreso  


def Dialog_OK(title, text):
    import xbmcgui
    xbmcgui.Dialog().ok(title,text)

def Dialog_YesNo(title, text):
    import xbmcgui
    return xbmcgui.Dialog().yesno(title,text)
    
def Dialog_Select(title, opciones): #----------------------------------OK
    import xbmcgui
    resultado = xbmcgui.Dialog().select(title, opciones)
    if resultado ==-1: resultado = None
    return resultado

def AddItem(item, title, thumbnail, mode): #----------------------------------OK
    contextCommands=[]   
    if "," in item.context:
      for menuitem in item.context.split("|"):
        if "," in menuitem:
          from copy import deepcopy
          Menu = deepcopy(item)
          if len(menuitem.split(",")) == 2:
            Titulo = menuitem.split(",")[0]
            Menu.action = menuitem.split(",")[1]
          elif len(menuitem.split(",")) == 3:
            Titulo = menuitem.split(",")[0]
            Menu.channel = menuitem.split(",")[1]
            Menu.action =menuitem.split(",")[2]
          Menu.refered_action = item.action
          contextCommands.append([Titulo,ConstruirURL(Menu)])
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    listitem.setInfo( "video", { "Title" : item.title, "Plot" : item.plot, "Studio" : item.channel} )
    if item.fanart!="":
      listitem.setProperty('fanart_image',item.fanart) 
      xbmcplugin.setPluginFanart(int(sys.argv[1]), item.fanart)
    listitem.addContextMenuItems (contextCommands, replaceItems=True)
    
    if item.folder:
      xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = sys.argv[ 0 ] + "?" + item.serialize() , listitem=listitem, isFolder=True)
    else:
      if config.get_setting("player_mode")=="1": # SetResolvedUrl debe ser siempre "isPlayable = true"
        listitem.setProperty('IsPlayable', 'true')
      xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = sys.argv[ 0 ] + "?" + item.serialize() , listitem=listitem, isFolder=False)
      

def CloseDirectory(refereditem): #----------------------------------OK
    import xbmc
    import xbmcplugin
    xbmcplugin.endOfDirectory( handle=int(sys.argv[1]), succeeded=True )
    if config.get_setting("forceview")=="true":
      if refereditem.viewmode=="list":
          xbmc.executebuiltin("Container.SetViewMode(50)")
      elif refereditem.viewmode=="movie_with_plot":
          xbmc.executebuiltin("Container.SetViewMode(503)")
      elif refereditem.viewmode=="movie":
          xbmc.executebuiltin("Container.SetViewMode(500)")    
    
    
def Refresh(): #----------------------------------OK
    import xbmc
    xbmc.executebuiltin( "Container.Refresh" )
    
def Keyboard(Texto, Title="", Password=False): #----------------------------------OK
    import xbmc

    keyboard = xbmc.Keyboard(Texto, Title, Password)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()
    else:
        return None
    
    
    
def play(item, ItemVideo):
    import xbmc
    import xbmcgui
    import xbmcplugin
    if not ItemVideo == None:
      mediaurl = ItemVideo.url[1]
      if len(ItemVideo.url)>2:
          wait_time = ItemVideo.url[2]
      else:
          wait_time = 0

      if wait_time>0:
        handle_wait(wait_time,server,"Cargando vídeo...")
        
      xlistitem = xbmcgui.ListItem( item.title, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail, path=mediaurl)
      xlistitem.setInfo( "video", { "Title": item.title, "Plot" : item.plot , "Studio" : item.channel , "Genre" : item.category } )

      if item.subtitle!="":
          import os
          ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
          if os.path.exists(ficherosubtitulo):
                os.remove(ficherosubtitulo)
      
          from core import scrapertools
          data = scrapertools.cache_page(item.subtitle)
          fichero = open(ficherosubtitulo,"w")
          fichero.write(data)
          fichero.close()
          

      if item.channel=="library": #Si es un fichero strm no hace falta el play
        xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,xlistitem)
        
      else:
        if config.get_setting("player_mode")=="3": #download_and_play
          import download_and_play
          download_and_play.download_and_play( mediaurl , "download_and_play.tmp" , config.get_setting("downloadpath"))
          
        elif config.get_setting("player_mode")=="0" or (config.get_setting("player_mode")=="3" and mediaurl.startswith("rtmp")): #Direct
        
          playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
          playlist.clear()
          playlist.add(mediaurl, xlistitem)
          playersettings = config.get_setting('player_type')
          player_type = xbmc.PLAYER_CORE_AUTO
          if playersettings == "0":
              player_type = xbmc.PLAYER_CORE_AUTO
              logger.info("[xbmctools.py] PLAYER_CORE_AUTO")
          elif playersettings == "1":
              player_type = xbmc.PLAYER_CORE_MPLAYER
              logger.info("[xbmctools.py] PLAYER_CORE_MPLAYER")
          elif playersettings == "2":
              player_type = xbmc.PLAYER_CORE_DVDPLAYER
              logger.info("[xbmctools.py] PLAYER_CORE_DVDPLAYER")
          xbmcPlayer = xbmc.Player(player_type)
          xbmcPlayer.play(playlist)
          
        elif config.get_setting("player_mode")=="1": #setResolvedUrl
          xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=mediaurl))
      
        elif config.get_setting("player_mode")=="2": #Built-in
          xbmc.executebuiltin( "PlayMedia("+mediaurl+")" )
    else:
      listitem = xbmcgui.ListItem( item.title, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail)
      xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,listitem)    # JUR Added
          
def Update(item):
    import xbmc
    if item.folder == True and "strm" in item.extra:
      listitem = xbmcgui.ListItem( None, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),False,listitem)    # JUR Added
    xbmc.executebuiltin(ConstruirURL(item).replace("XBMC.RunPlugin","Container.Update"))

def UpdateLibrary(item):
    import xbmc
    xbmc.executebuiltin('UpdateLibrary(video)')

def ConstruirURL(item):
    return "XBMC.RunPlugin("+sys.argv[ 0 ] + "?" + item.serialize()+")" 
    
def ConstruirStrm(item):
    return sys.argv[ 0 ] + "?" + item.serialize() 