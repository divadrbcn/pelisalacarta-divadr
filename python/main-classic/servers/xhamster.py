# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
from core import logger
from core import scrapertools

def get_video_url(page_url, video_password):
    video_urls = []
    media_url =""

    data = scrapertools.cachePage(page_url)

    data = scrapertools.get_match(data,'sources: (.*?),\n')
    logger.info(data)
    import json
    JsonUrl = json.loads(data)
    for key in JsonUrl:
      video_urls.append( [ scrapertools.get_filename_from_url(JsonUrl[key][0].encode("utf8"))[-4:]+" [xhamster] " + "[" + key.encode("utf8") + "]", JsonUrl[key].encode("utf8")])
    
    return video_urls
    
def find_videos(data):
    devuelve = []
    patronvideos  = 'xhamster.com/xembed.php\?video=([0-9]+)'
    logger.info("[xhamster.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    logger.info(matches)
    for match in matches:
        url = "http://xhamster.com/xembed.php?video="+match
        titulo = "[xhamster]"
        devuelve.append( [ titulo , url , 'xhamster'] )
    return devuelve