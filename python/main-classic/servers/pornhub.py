# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para pornhub
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
from core import logger
from core import scrapertools

def get_video_url(page_url, video_password):
    video_urls = []
    data = scrapertools.cachePage(page_url)
    media_url = scrapertools.get_match(data,"src		: '([^']+)',")
    
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [pornhub] ", media_url])

    return video_urls
    
def find_videos(data):
    devuelve = []
    patronvideos  = 'http://es.pornhub.com/embed/([0-9]+)'
    logger.info("[pornhub.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    logger.info(matches)
    for match in matches:
        url = "http://es.pornhub.com/embed/"+match
        titulo = "[pornhub]"
        devuelve.append( [ titulo , url , 'pornhub'] )
    return devuelve