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
from core import config
from core.item import Item
 
def ExtraerItem():
    itemserializado = sys.argv[2].replace("?","")




class DialogoProgreso(object):
  Progreso=""
  Titulo=""
  Closed=False
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
    self.Closed = False
  def IsCanceled(self):
        return (self.Progreso.isCanceled() or self.Closed)
  
  def Actualizar(self,Porcentaje, Texto):
        self.Progreso.update(Texto, Porcentaje)

  
  def Cerrar(self):
        self.Progreso.close()
        self.Closed = True
        
class DialogoProgresoBG(object):
  Progreso=""
  Titulo=""
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
  
  def Actualizar(self,Porcentaje, Texto):
        self.Progreso.update(Porcentaje, self.Titulo, Texto)

  
  def Cerrar(self):
        self.Progreso.close()


def isPlaying():
    import xbmc
    return xbmc.Player().isPlaying()
    
    
def Dialog_Progress(title, Texto):
    import ui
    progreso = ui.WindowDialog(title, Texto,0)
    Progreso = DialogoProgreso(progreso,title)
    return Progreso

def Dialog_ProgressBG(title, Texto):
    import xbmcgui
    progreso = xbmcgui.DialogProgressBG()
    progreso.create(title, Texto)
    Progreso = DialogoProgresoBG(progreso,title)
    return Progreso    


def Dialog_OK(title, text):
    import ui
    ui.OKWindow("DialogOk.xml",config.get_runtime_path()).show(title,text)
 

def Dialog_YesNo(title, text):
    import ui
    return ui.YesNoWindow("YesNoDialog.xml",config.get_runtime_path()).show(title,text)
    
def Dialog_Select(title, opciones): #----------------------------------OK
    import ui
    resultado = ui.SelectWindow("ListDialog.xml",config.get_runtime_path()).setOptions(title, opciones)
    if resultado ==-1: resultado = None
    return resultado

def AddItem(item, totalitems=0): #----------------------------------OK
  pass      

def CloseDirectory(refereditem): #----------------------------------OK
  pass

    
    
    
def Refresh(): #----------------------------------OK
    import ui
    ui.WindowXML.LoadItem(ui.WindowXML.item)
    
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
        pass
    
      elif config.get_setting("player_mode")=="2": #Built-in
        xbmc.executebuiltin( "PlayMedia("+mediaurl+")" )
          
def Update(item):
  import ui
  ui.WindowXML.LoadItem(item)

def UpdateLibrary(item):
    import xbmc
    xbmc.executebuiltin('UpdateLibrary(video)')

    
def ConstruirURL(item):
  pass
    
def ConstruirStrm(item):
    return sys.argv[ 0 ] + "?" + item.serialize() 

