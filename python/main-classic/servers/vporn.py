# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vporn
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
from core import logger
from core import scrapertools

def get_video_url(page_url, video_password):
    video_urls = []
    media_url =""
    videoid= scrapertools.get_match(page_url,'http://www.vporn.com/embed/([0-9]+)')
    data = scrapertools.cachePage("http://www.vporn.com/xml/video.php?id="+videoid)
    
    patronvideos  = '<videoUrl[^>]+>([^<]+)</videoUrl[^>]+>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for url in matches:
      resolucion, k = scrapertools.get_match(url,videoid+'_([^_]+)_([^.]+)')
      video_urls.append( [ scrapertools.get_filename_from_url(url)[-4:]+" [vporn] " + "[" + resolucion + "]", url])

    
    return video_urls
    
def find_videos(data):
    devuelve = []
    patronvideos  = 'http://www.vporn.com/embed/([0-9]+)'
    logger.info("[vporn.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    logger.info(matches)
    for match in matches:
        url = "http://www.vporn.com/embed/"+match
        titulo = "[vporn]"
        devuelve.append( [ titulo , url , 'vporn'] )
    return devuelve