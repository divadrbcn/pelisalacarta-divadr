# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mega.co.nz
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import random
import sys
import urlparse,urllib2,urllib,re
import os
from core import scrapertools
from core import logger
from core import config

#Temporal para actualizar megaserver
import hashlib
megaserverpath = os.path.join(config.get_runtime_path(),"core","megaserver.py")
if hashlib.sha1(open(megaserverpath, 'rb').read()).hexdigest() <> "d6c2f83fb149df8148df24ed1a54fb28641f84e1":
  if config.get_setting("branch"):
    branch = config.get_setting("branch")
  else:
    branch = "master"
    
  downloadurl = "https://raw.githubusercontent.com/divadres/pelisalacarta/"+branch+"/pelisalacarta/core/megaserver.py"
  data = scrapertools.cachePage(downloadurl)
  #logger.error( hashlib.sha1(open(megaserverpath, 'rb').read()).hexdigest())
  open(megaserverpath,"wb").write(data)

try:
  from core import megaserver
except:
  megaserver = None

def test_video_exists( page_url ):
    logger.info("[mega.py] test_video_exists(page_url='%s')" % page_url)
    
    if "#!" in page_url or "#F!" in page_url or "#N!" in page_url:
      return True,""
    else:
      return False,"¡El enlace no está soportado!"


def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mega.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.mimediacenter.info', 80))
    myip = s.getsockname()[0]
    puerto = random.randint(0, 0xFFFF)
    mega = megaserver.MEGAServer()

    if "#!" in page_url:
      file = mega.get_filename(page_url).encode("utf8")
      size = "%.1f%s" % ChangeUnits(mega.get_size(page_url))
      url = "http://"+myip+":"+str(puerto)+"/mega"+file[-4:]+"?"+page_url.split("#")[1]
      video_urls.append( [ "("+size+") " + scrapertools.get_filename_from_url(url)[-4:]+" [mega]",url])
    
    elif "#F!" in page_url:
      files = mega.get_files(page_url)
      for file in files:
        url = "http://"+myip+":"+str(puerto)+"/mega"+file["name"][-4:]+"?"+ file["url"]
        url = url.encode("utf8")
        name = file["name"].encode("utf8")
        size = "%.1f%s" % ChangeUnits(file["size"])
        video_urls.append( [ " ("+size+") " + scrapertools.get_filename_from_url(url)[-4:]+" [mega]",url])
        
    elif "#N!" in page_url:
      file = mega.get_filename(page_url).encode("utf8")
      size = "%.1f%s" % ChangeUnits(mega.get_size(page_url))
      url = "http://"+myip+":"+str(puerto)+"/mega"+file[-4:]+"?"+page_url.split("#")[1]
      video_urls.append( [ "("+size+") " + scrapertools.get_filename_from_url(url)[-4:]+" [mega]",url])

    
    else:
      pass
    mega.start(puerto)
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    mega = megaserver.MEGAServer()
    #https://mega.co.nz/#!TNBl0CbR!S0GFTCVr-tM_cPsgkw8Y-0HxIAR-TI_clqys
    patronvideos  = '(mega(?:.co)?.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)   
             
    #https://mega.co.nz/#!TNBl0CbR!S0GFTCVr-tM_cPsgkw8Y-0HxIAR-TI_clqys
    patronvideos  = '(mega(?:.co)?.nz/\#F\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        folder_url="https://"+match
        files = mega.get_files(folder_url)
        
        for file in files:
          url = folder_url.split("#")[0]+"#N"+ file["url"]
          
          url = url.encode("utf8")
          name = file["name"].encode("utf8")
          if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [name , url , 'mega' ] )
            encontrados.add(url)
          else:
            logger.info("  url duplicada="+url)   
 
    return devuelve

def ChangeUnits(value=0):
  Unidades = ["Bytes", "KB", "MB", "GB"]
  Retorno = float(value)
  x=0
  while Retorno >= 1024:
    Retorno = Retorno / 1024
    x+=1
  Unidad = Unidades[x]
  return Retorno, Unidad