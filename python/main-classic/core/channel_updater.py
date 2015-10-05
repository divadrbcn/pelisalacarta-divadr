# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# update_servers.py
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os
import sys
from core import scrapertools
from core import config
from core import logger
import json

DEBUG = config.get_setting("debug")
headers = [["User-Agent", "pelisalacarta"]] 
GitApi = "https://api.github.com/repos/tvalacarta/pelisalacarta/contents/python/main-classic/"


### Procedures
def Check():
  import guitools
  progress = guitools.Dialog_ProgressBG("Pelisalacarta","Comprobando actualizaciones...")

  DownloadServers = []
  DownloadChannels = []
  ServersPath = os.path.join( config.get_runtime_path(), "servers" )
  ServersIndexPath = os.path.join(config.get_data_path(), "Servers.json")
  ChannelsPath = os.path.join( config.get_runtime_path(), "channels" )
  ChannelsIndexPath = os.path.join(config.get_data_path(), "Channels.json")
  if not os.path.isfile(ServersIndexPath): CreateIndex(ServersIndexPath,"servers")
  if not os.path.isfile(ChannelsIndexPath): CreateIndex(ChannelsIndexPath,"channels")
  
  #Servers
  progress.Actualizar(25, "Descargando lista de Servidores...")
  RemoteJSONData = json.loads(scrapertools.cache_page(GitApi + "servers", headers=headers))
  LocalJSONData = json.loads(open(ServersIndexPath,"r").read())

  if RemoteJSONData <> LocalJSONData:
    for Server in RemoteJSONData:
      if not Server in LocalJSONData:
        DownloadServers.append(Server)
        
  #Channels
  progress.Actualizar(50, "Descargando lista de Canales...")
  RemoteJSONData = json.loads(scrapertools.cache_page(GitApi + "channels", headers=headers))
  LocalJSONData = json.loads(open(ChannelsIndexPath,"r").read())

  progress.Actualizar(75, "Comprobando...")
  if RemoteJSONData <> LocalJSONData:
    for Channel in RemoteJSONData:
      if not Channel in LocalJSONData:
        DownloadChannels.append(Channel)
               
  if DownloadServers or DownloadChannels:    
    
    for File in  DownloadServers:   
      Progreso = DownloadServers.index(File) * 100 / (len(DownloadServers) + len(DownloadChannels))
      progress.Actualizar(Progreso ,'Actualizando Archivo: "' + File["name"] + '"')
      open(os.path.join(config.get_runtime_path(), "servers", File["name"]),"wb").write(scrapertools.cachePage(File["download_url"]))
    for File in  DownloadChannels:   
      Progreso = (DownloadChannels.index(File) + len(DownloadServers)  ) * 100 / (len(DownloadServers) + len(DownloadChannels))
      progress.Actualizar(Progreso ,'Actualizando Archivo: "' + File["name"] + '"')
      open(os.path.join(config.get_runtime_path(), "channels", File["name"]),"wb").write(scrapertools.cachePage(File["download_url"]))
      
    CreateIndex(ServersIndexPath,"servers")
    CreateIndex(ChannelsIndexPath,"channels")

  progress.Actualizar(100, "Todos los canales y servidores estan actualizados")
  import time
  time.sleep(3)
  progress.Cerrar()
 
  
def CreateIndex(IndexPath, Folder):
    import hashlib
    logger.info("Creando indice de: " + Folder)
    JSONData=[]
    
    for File in os.listdir(os.path.join(config.get_runtime_path(), Folder)):
      File = os.path.join(config.get_runtime_path(), Folder,File)
      if not File.endswith(".pyc"):
          FileData = open(File, 'rb').read()
          JSONFile={}
          JSONFile["name"] = os.path.basename(File)
          JSONFile["size"] = len(FileData)
          JSONFile["path"] = "python/main-classic/"+Folder + "/" + JSONFile["name"]
          JSONFile["url"] = "https://api.github.com/repos/tvalacarta/pelisalacarta/contents/" + JSONFile["path"] + "?ref=master"
          JSONFile["type"] = "file"
          JSONFile["sha"] =  hashlib.sha1("blob " + str(JSONFile["size"]) + "\0" + FileData).hexdigest()
          JSONFile["download_url"] = "https://raw.githubusercontent.com/tvalacarta/pelisalacarta/master/" + JSONFile["path"] 
          JSONFile["git_url"] = "https://api.github.com/repos/tvalacarta/pelisalacarta/git/blobs/" + JSONFile["sha"]
          JSONFile["html_url"] = "https://github.com/tvalacarta/pelisalacarta/blob/master/"+ JSONFile["path"]
          JSONFile["_links"]={}
          JSONFile["_links"]["git"] = JSONFile["git_url"]
          JSONFile["_links"]["html"] = JSONFile["html_url"]
          JSONFile["_links"]["self"] = JSONFile["url"] 
          JSONData.append(JSONFile)
    JSONData.sort(key=lambda item: item["name"])
    open(IndexPath,"w").write(json.dumps(JSONData, indent=4, sort_keys=True))