#! /usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys
sys.dont_write_bytecode = True

import os
from core import logger
from core import config
from core.item import Item
from threading import Thread
import threading
import navigation
from core import guitools
import socket

librerias = os.path.join( config.get_runtime_path(), 'lib' ) 
sys.path.append (librerias)
sys.argv ={}
PORT=int(config.get_setting("server.port"))
WebsocketPort=int(config.get_setting("websocket.port"))  
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.mimediacenter.info', 80))
    myip = s.getsockname()[0]
except:
    myip = "0.0.0.0"
   
def ReloadModules():
  if 0:
    import inspect
    #Recorre los modulos cargados en memoria
    for module in sys.modules.keys():
      if inspect.ismodule(sys.modules[module]):
        #Recarga todos los modulos excepto los loggers.
        if config.get_runtime_path() in str(sys.modules[module]) and not "__main__" in str(sys.modules[module]) and not "logger" in str(sys.modules[module]) and not "library_service" in str(sys.modules[module]):
          reload(sys.modules[module])

def ProcessRequest(Socket):
  sys.argv[threading.current_thread().name]={"Socket":str(Socket), "Thread": threading.current_thread()}
  sys.argv[str(Socket)]["Host"] = "http://"+ myip + ":" + str(PORT)
  MostrarInfo()
  ReloadModules()
          
  try:
    itemserializado = sys.argv[sys.argv[threading.current_thread().name]["Socket"]]["Request"]
    if itemserializado:
      item = Item()
      item.deserialize(itemserializado)
    else:
      item = Item(channel="channelselector", action="mainlist")
    logger.info("-----------------------------------------------------------------------")
    logger.info("Item Recibido: " + item.tostring())
    logger.info("-----------------------------------------------------------------------")
    
    if (item.channel=="channelselector" and item.action=="mainlist") or (item.channel=="novedades" and item.action=="mainlist") or (item.channel=="buscador" and item.action=="mainlist") or (item.channel=="channelselector" and item.action=="channeltypes"):
      WindowMode = 0
    elif item.channel=="channelselector" and item.action=="listchannels":
      WindowMode = 1
    else:
      WindowMode = 2
      
    itemlist = navigation.NextItem(item)
    if type(itemlist)==list: 
      if not (item.channel=="channelselector" and item.action=="mainlist") and not itemlist[0].action=="go_back":
        itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail="%sthumb_atras.png"))


      for x in range(len(itemlist)):
        nitem, title, thumbnail = navigation.ItemInfo(item, itemlist[x], WindowMode)
        guitools.AddItem(nitem, title, thumbnail, WindowMode)        
      guitools.CloseDirectory(item)
      
    del sys.argv[threading.current_thread().name]
    MostrarInfo()
    
  except Exception as e:
    import traceback
    from platformcode import cliente
    logger.error(traceback.format_exc())
    from core import scrapertools
    patron = 'File "'+os.path.join(config.get_runtime_path(),"pelisalacarta","channels","").replace("\\","\\\\")+'([^.]+)\.py"'
    canal = scrapertools.find_single_match(traceback.format_exc(),patron)
    if canal:
      cliente.Dialogo().MostrarOK(
        "Se ha producido un error en el canal " + canal,
        "Esto puede ser devido a varias razones: \n - El servidor no está disponible, o no esta respondiendo.\n - Cambios en el diseño de la web.\n - Etc...\nComprueba el log para ver mas detalles del error.")
    else:
      cliente.Dialogo().MostrarOK(
        "Se ha producido un error en pelisalacarta",
        "Comprueba el log para ver mas detalles del error." )
    del sys.argv[threading.current_thread().name]
    MostrarInfo()

def MostrarInfo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("--------------------------------------------------------------------")
    print ("Pelisalacarta Iniciado")
    print ("La URL para acceder es http://" + myip + ":" + str(PORT))
    print ("WebSocket Server iniciado en ws://"+ myip + ":" + config.get_setting("websocket.port")+"/")
    print ("--------------------------------------------------------------------")
    print ("Runtime Path      : " + config.get_runtime_path())
    print ("Data Path         : " + config.get_data_path())
    print ("Download Path     : " + config.get_setting("downloadpath") )
    print ("DownloadList Path : " + config.get_setting("downloadlistpath"))
    print ("Bookmark Path     : " + config.get_setting("bookmarkpath"))  
    print ("Library Path      : " + config.get_setting("library_path"))  
    print ("Cache Path        : " + config.get_setting("cache.dir"))  
    print ("Cookies Path      : " + config.get_setting("cookies.dir"))  
    print ("--------------------------------------------------------------------")
    conexiones = []
    Threads = []
    for a in sys.argv:
      if "WebSocket" in a:
        try:
          conexiones.append(str(sys.argv[a]["Socket"].client.getpeername()).split("'")[1])
        except:
          del sys.argv[a]
      if "Thread" in a:
        Threads.append(a)
    if len(conexiones) >0:
      print ("Clientes conectados:")
      for conexion in conexiones:
        print (conexion)
    else:
      print ("No hay conexiones")
      
    if len(Threads) >0:
      print ("")
      print ("Hilos Trabajando:")
      for Thr in Threads:
        print (Thr)
    else:
      print ("")
      print ("No hay Hilos")


def start():
  logger.info("pelisalacarta server init...")
  config.verify_directories_created() 
  try: 
      import HTTPServer
      HTTPServer.start()
      import WebSocket
      WebSocket.start(ProcessRequest,MostrarInfo)
      
        
      # Da por levantado el servicio
      logger.info("--------------------------------------------------------------------")
      logger.info("Pelisalacarta Iniciado")
      logger.info("La URL para acceder es http://" + myip + ":" + str(PORT))
      logger.info("WebSocket Server iniciado en ws://"+ myip + ":" + str(WebsocketPort))
      logger.info("--------------------------------------------------------------------")
      logger.info("Runtime Path      = " + config.get_runtime_path())
      logger.info("Data Path         = " + config.get_data_path())
      logger.info("Download Path     = " + config.get_setting("downloadpath") )
      logger.info("DownloadList Path = " + config.get_setting("downloadlistpath"))
      logger.info("Bookmark Path     = " + config.get_setting("bookmarkpath"))
      logger.info("Library Path      = " + config.get_setting("library_path"))
      logger.info("Cache Path        : " + config.get_setting("cache.dir"))  
      logger.info("Cookies Path      : " + config.get_setting("cookies.dir"))  
      logger.info("--------------------------------------------------------------------")
      MostrarInfo()
      
      Start = True
      while Start:
        pass
  except KeyboardInterrupt:
      print 'Deteniendo el servidor'
      HTTPServer.stop()
      WebSocket.stop()
      Start= False

#Inicia pelisalacarta
start()