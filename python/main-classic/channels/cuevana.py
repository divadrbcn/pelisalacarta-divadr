﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__active__ = True
__adult__ = False
__category__ = "F"
__changes__ = "Actualizado por cambios en el canal"
__channel__ = "cuevana"
__creationdate__ = ""
__date__ = "05/05/2012"
__language__ = "ES"
__thumbnail__ = ""
__title__ = "Cuevana"
__type__ = "generic"
__version__ = 26

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cuevana mainlist")
    itemlist = []
    
    item.url = "http://cuevana3.com.ar/"

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas
    patron  = '<li[^<]+'
    patron += '<a  title="([^"]+)" href="([^"]+)"><img class="panel" src="([^"]+)"[^<]+</a[^<]+'
    patron += '</li>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        title = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title, fulltitle=title , url=url , thumbnail=thumbnail) )

    next_page_url = scrapertools.find_single_match(data,'<a class="nextpostslink" rel="next" href="([^"]+)">')
    if next_page_url!="":
        itemlist.append( Item(channel=__channel__, action="novedades", title="Página siguiente >>" , url=scrapedurl) )

    return itemlist
