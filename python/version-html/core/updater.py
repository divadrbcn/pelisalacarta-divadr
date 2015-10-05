# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta
# XBMC Plugin
#------------------------------------------------------------

import re
import os
import sys
import scrapertools
import config
import logger
import json
from core.item import Item
import guitools

if config.get_setting("branch"):
  branch = config.get_setting("branch")
else:
  branch = "master"
  
channelspath = os.path.join(config.get_data_path(), "Channels.json")
serverspath = os.path.join(config.get_data_path(), "Servers.json")
lastupdatepath = os.path.join(config.get_data_path(), "update.txt")

giturl = "https://api.github.com/repos/divadres/pelisalacarta/contents"
downloadurl = "https://raw.githubusercontent.com/divadres/pelisalacarta/"+branch
headers = [["User-Agent", "pelisalacarta"]]  

def checkforupdates(): 
  import time
  logger.info("checkforupdates")
  
  #Actualizaciones del plugin
  if config.get_setting("updatecheck2") == "true":
    logger.info("Comprobando actualizaciones de pelisalcarta")
    if os.path.isfile(lastupdatepath): 
      UltimaConsulta = float(open(lastupdatepath,"rb").read())
    else:
      UltimaConsulta = 0
    if int(time.time() - UltimaConsulta) > 3600:
    
      REMOTE_VERSION_FILE = downloadurl + "/update/version.xml"
      LOCAL_VERSION_FILE = os.path.join( config.get_runtime_path(), "version.xml" )
      data = scrapertools.cachePage(REMOTE_VERSION_FILE)

      if data:
        patron  = '<tag>([^<]+)</tag>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        versiondescargada = matches[0]
      else:
        versiondescargada = 0
        
      data = open(LOCAL_VERSION_FILE).read()
      matches = re.compile(patron,re.DOTALL).findall(data)
      versionlocal = matches[0]
      
      logger.info("Versión local: " + versionlocal)
      logger.info("Versión remota: " + versiondescargada)
      
      from distutils.version import StrictVersion
      if StrictVersion(versiondescargada) > StrictVersion(versionlocal):
        if guitools.Dialog_YesNo("pelisalacarta","¡Hay una nueva versión lista para descargar!\nVersión actual: "+versionlocal+" - Nueva versión: "+versiondescargada+"\nQuieres instalarla ahora?"):
          update(Item(url=versiondescargada))
        else:
         if guitools.Dialog_YesNo("pelisalacarta","¿No volver a mostrar en una hora?"):
            open(lastupdatepath,"wb").write(str(time.time()))
            logger.info("Opciñon seleccionada: No Descargar")
    else:
        logger.info("No preguntar hasta: " + str(3600 - int(time.time() - UltimaConsulta)) + " Segundos" )
        
  #Actualizacion de canales      
  if config.get_setting("updatechannels") == "true":
    logger.info("Comprobando actualizaciones de canales")
    data = scrapertools.cache_page(giturl + "/pelisalacarta/pelisalacarta/channels?ref="+branch, headers=headers)
    RemoteJSONData = json.loads(data)
    
    if not os.path.isfile(channelspath): CreateChannelsIndex()
    f = open(channelspath,"r")
    JSONData = json.loads(f.read())
    f.close()

    downloadchannels=[]
    if RemoteJSONData == JSONData:
      logger.info("Todos los canales estan actualizados")
    else:
      logger.info("Hay canales para actualizar")
      for file in RemoteJSONData:
        if not file in JSONData:
          
          downloadchannels.append(file)
          
    logger.info("Comprobando actualizaciones de servers")
    data = scrapertools.cache_page(giturl + "/pelisalacarta/servers?ref="+branch, headers=headers)
    RemoteJSONData = json.loads(data)
    
    if not os.path.isfile(serverspath): CreateServersIndex()
    f = open(serverspath,"r")
    JSONData = json.loads(f.read())
    f.close()

    downloadservers=[]
    if RemoteJSONData == JSONData:
      logger.info("Todos los servers estan actualizados")
    else:
      logger.info("Hay servers para actualizar")
      for file in RemoteJSONData:
        if not file in JSONData:
          downloadservers.append(file)

    if downloadchannels or downloadservers:
        dialog = guitools.Dialog_Progress("Actualizando...","")
        
        for file in downloadchannels:
          if dialog.IsCanceled(): break
          logger.info("Actualizando: " + file["name"])
          dialog.Actualizar(downloadchannels.index(file)*100 / (len(downloadchannels) + len(downloadservers)), "Actualizando canal: " + file["name"].encode("utf8")) 
          data = scrapertools.cachePage(file["download_url"])
          open(os.path.join(config.get_runtime_path(), "..", *file["path"].split("/")),"wb").write(data)
          import inspect 
          for module in sys.modules.keys(): 
            if inspect.ismodule(sys.modules[module]): 
              if file["name"].encode("utf8").replace(".py","") in module:
                reload(sys.modules[module]) 

        for file in downloadservers:
          if dialog.IsCanceled(): break
          logger.info("Actualizando: " + file["name"])
          dialog.Actualizar((downloadservers.index(file) + len(downloadchannels)) *100 / (len(downloadchannels) + len(downloadservers)), "Actualizando server: " + file["name"].encode("utf8")) 
          data = scrapertools.cachePage(file["download_url"])
          open(os.path.join(config.get_runtime_path(), "..", *file["path"].split("/")),"wb").write(data)
          import inspect 
          for module in sys.modules.keys(): 
            if inspect.ismodule(sys.modules[module]): 
              if file["name"].encode("utf8").replace(".py","") in module:
                reload(sys.modules[module]) 

        
        if dialog.IsCanceled(): 
          dialog.Cerrar()
          CreateChannelsIndex()
          CreateServersIndex()
          guitools.Dialog_OK("Actualizaciones", "¡El proceso se ha cancelado!" )

        else:
          dialog.Cerrar()
          CreateChannelsIndex()
          CreateServersIndex()
          guitools.Dialog_OK("Actualizaciones", "¡Canales descargados con éxito!" )
          

def CreateChannelsIndex():
    logger.info("Creando indice de canales")
    import hashlib
    JSONData=[]
    for channel in os.listdir(os.path.join(config.get_runtime_path() ,"pelisalacarta","channels","")):
      channel = os.path.join(os.path.join(config.get_runtime_path() ,"pelisalacarta","channels",channel))
      if channel.endswith(".py"):
          channeldata = open(channel, 'rb').read().replace("\r\n","\n")
          JSONChannel={}
          JSONChannel["name"] = os.path.basename(channel)
          JSONChannel["size"] = len(channeldata)
          path = os.path.dirname(config.get_runtime_path())
          if not path.endswith(os.sep): path +=os.sep
          
          JSONChannel["path"] = "/".join(channel.replace(path,"",1).split(os.sep))
          JSONChannel["url"] = "https://api.github.com/repos/divadres/pelisalacarta/contents/" +JSONChannel["path"] +"?ref=" + branch
          JSONChannel["type"] = "file"
          JSONChannel["sha"] =  hashlib.sha1("blob " + str(JSONChannel["size"]) + "\0" + channeldata).hexdigest()
          JSONChannel["download_url"] = "https://raw.githubusercontent.com/divadres/pelisalacarta/"+ branch + "/" + JSONChannel["path"] 
          JSONChannel["git_url"] = "https://api.github.com/repos/divadres/pelisalacarta/git/blobs/" + JSONChannel["sha"]
          JSONChannel["html_url"] = "https://github.com/divadres/pelisalacarta/blob/"+ branch + "/"+ JSONChannel["path"]
          JSONChannel["_links"]={}
          JSONChannel["_links"]["git"] = JSONChannel["git_url"]
          JSONChannel["_links"]["html"] = JSONChannel["html_url"]
          JSONChannel["_links"]["self"] = JSONChannel["url"] 
          JSONData.append(JSONChannel)
    JSONData.sort(key=lambda item: item["name"])
    open(channelspath,"w").write(json.dumps(JSONData, indent=4, sort_keys=True))

def CreateServersIndex():
    logger.info("Creando indice de servers")
    import hashlib
    JSONData=[]
    for server in os.listdir(os.path.join(config.get_runtime_path() ,"servers","")):
      server = os.path.join(os.path.join(config.get_runtime_path() ,"servers",server))
      if server.endswith(".py"):
          serverdata = open(server, 'rb').read().replace("\r\n","\n")
          JSONServer={}
          JSONServer["name"] = os.path.basename(server)
          JSONServer["size"] = len(serverdata)
          path = os.path.dirname(config.get_runtime_path())
          if not path.endswith(os.sep): path +=os.sep
          JSONServer["path"] = "/".join(server.replace(path,"",1).split(os.sep))
          JSONServer["url"] = "https://api.github.com/repos/divadres/pelisalacarta/contents/" +JSONServer["path"] +"?ref=" + branch
          JSONServer["type"] = "file"
          JSONServer["sha"] =  hashlib.sha1("blob " + str(JSONServer["size"]) + "\0" + serverdata).hexdigest()
          JSONServer["download_url"] = "https://raw.githubusercontent.com/divadres/pelisalacarta/"+ branch + "/" + JSONServer["path"] 
          JSONServer["git_url"] = "https://api.github.com/repos/divadres/pelisalacarta/git/blobs/" + JSONServer["sha"]
          JSONServer["html_url"] = "https://github.com/divadres/pelisalacarta/blob/"+ branch + "/"+ JSONServer["path"]
          JSONServer["_links"]={}
          JSONServer["_links"]["git"] = JSONServer["git_url"]
          JSONServer["_links"]["html"] = JSONServer["html_url"]
          JSONServer["_links"]["self"] = JSONServer["url"] 
          JSONData.append(JSONServer)
    JSONData.sort(key=lambda item: item["name"])
    open(serverspath,"w").write(json.dumps(JSONData, indent=4, sort_keys=True))


def update(item):
    logger.info("Actualizando plugin...")   
    
    LOCAL_FILE = os.path.join( config.get_runtime_path(), "..","pelisalacarta-"+item.url+".zip" )
    REMOTE_FILE = downloadurl + "/update/pelisalacarta-mediaserver-"+item.url+".zip"
    DESTINATION_FOLDER = os.path.join(config.get_runtime_path(),"..")

    logger.info("Archivo Remoto: " + REMOTE_FILE)
    logger.info("Archivo Local: " + LOCAL_FILE)
    
    from core import downloadtools
    if os.path.isfile(LOCAL_FILE):
      os.remove(LOCAL_FILE)
    ret = downloadtools.downloadfile(REMOTE_FILE, LOCAL_FILE)
    if ret is None:
      logger.info("Descomprimiendo fichero...")
      import ziptools
      unzipper = ziptools.ziptools()
      logger.info("Destino: " + DESTINATION_FOLDER)
      
      if os.path.isfile(channelspath): os.remove(channelspath)
      if os.path.isfile(serverspath): os.remove(serverspath)
      if os.path.isfile(lastupdatepath): os.remove(lastupdatepath)
      
      import shutil
      for file in os.listdir(os.path.join(DESTINATION_FOLDER,"pelisalacarta")):
        if not file in [".",".."]:
          if os.path.isdir(os.path.join(DESTINATION_FOLDER,"pelisalacarta", file)):
            shutil.rmtree(os.path.join(DESTINATION_FOLDER,"pelisalacarta", file))
          if os.path.isfile(os.path.join(DESTINATION_FOLDER,"pelisalacarta", file)):
            os.remove(os.path.join(DESTINATION_FOLDER,"pelisalacarta", file))
          pass
     
      unzipper.extract(LOCAL_FILE,DESTINATION_FOLDER)
      os.remove(LOCAL_FILE)
      guitools.Dialog_OK("Actualizacion", "Pelisalacarta se reiniciara\nEspera 20 segundos y actualiza la página.")
      os._exit(0)
    else:
      guitools.Dialog_OK("Actualizacion", "Se ha producido un error al descargar el archivo")
