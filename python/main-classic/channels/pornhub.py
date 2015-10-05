# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pornhub
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

#Propiedades del Canal:
__active__ = True
__adult__ = True
__category__ = "X,F"
__changes__ = "Primera version"
__channel__ = "pornhub"
__creationdate__ = ""
__date__ = "05/10/15"
__fanart__ = "http://i.imgur.com/PwFvoss.jpg"
__language__ = "ES"
__thumbnail__ = "http://s22.postimg.org/5lzcocfqp/pornhub_logo.jpg"
__title__ = "PornHub"
__type__ = "generic"
__version__ = 2

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
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="peliculas"    , title="Todos"          , url="http://es.pornhub.com/video", fanart=__fanart__))
    itemlist.append( Item(channel=__channel__, action="generos"      , title="Por Generos"    , url="http://es.pornhub.com/categories" , fanart=__fanart__))
    itemlist.append( Item(channel=__channel__, action="search"       , title="Buscar..."      , url="http://es.pornhub.com/video/search?search=", fanart=__fanart__ ))

    return itemlist

def search(item,texto):
  item.url = item.url + texto
  return buscar(item)





def generos(item):
    logger.info("[pornhub.py] generos")
    itemlist = []
   
    # Descarga la página
    data = scrapertools.downloadpage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.find_single_match(data,'<div id="categoriesStraightImages">(.*?)</ul>')
    # Extrae las categorias
    patron  = '<li class="cat_pic" data-category="\d+">.*?'
    patron += '<a href="([^"]+)">'
    patron += '<img src="([^"]+)" '
    patron += 'alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle
        if "?" in scrapedurl:
          url = urlparse.urljoin(item.url,scrapedurl + "&o=cm")
        else:
          url = urlparse.urljoin(item.url,scrapedurl + "?o=cm")
          
        thumbnail = urllib.quote(scrapedthumbnail, safe="%/:&?")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title, url=url , fanart=__fanart__ , thumbnail=thumbnail) )
        itemlist.sort(key=lambda x: x.title)
    return itemlist

def peliculas(item):
    logger.info("[pornhub.py] peliculas")
    itemlist = []
       
    # Descarga la página
    data = scrapertools.downloadpage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.find_single_match(data,'<ul class="nf-videos videos row-4-thumbs">(.*?)<div class="pre-footer">')
    # Extrae las peliculas
    patron = '<div class="phimage">.*?'
    patron += '<a href="/view_video.php\?viewkey=([^"]+)" title="([^"]+).*?'
    patron += '<var class="duration">([^<]+)</var>(.*?)</div>.*?'
    patron += 'data-smallthumb="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for viewkey,scrapedtitle,duration,scrapedhd,thumbnail in matches:       
        title=scrapedtitle
        scrapedhd = scrapertools.find_single_match(scrapedhd,'<span class="hd-thumbnail">(.*?)</span>')
        url= 'http://es.pornhub.com/embed/' + urllib.quote(viewkey, safe="%/:&?")
        thumbnail = urllib.quote(thumbnail, safe="%/:&?")        
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url , duration=duration, quality=scrapedhd,fanart=__fanart__, thumbnail=thumbnail) )
        
    # Paginador
    patron = '<li class="page_next"><a href="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        url=urlparse.urljoin("http://es.pornhub.com",matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Página siguiente >" ,fanart=__fanart__, url=url)) 
    return itemlist
    
def buscar(item):
    logger.info("[pornhub.py] buscar")
    itemlist = []
       
    # Descarga la página
    data = scrapertools.downloadpage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.find_single_match(data,'<ul class="videos row-4-thumbs">(.*?)<div class="pre-footer">')
    # Extrae las peliculas
    patron = '<div class="phimage">.*?'
    patron += '<a href="/view_video.php\?viewkey=([^"]+)" title="([^"]+).*?'
    patron += '<var class="duration">([^<]+)</var>(.*?)</div>.*?'
    patron += 'data-smallthumb="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for viewkey,scrapedtitle,duration,scrapedhd,thumbnail in matches:       
        title=scrapedtitle +" ("+duration+")"
        scrapedhd = scrapertools.find_single_match(scrapedhd,'<span class="hd-thumbnail">(.*?)</span>')
        if (scrapedhd == 'HD') : title += ' [HD]'
        url= 'http://es.pornhub.com/embed/' + urllib.quote(viewkey, safe="%/:&?")
                
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=title , url=url ,fanart=__fanart__, thumbnail=thumbnail) )
        
    # Paginador
    patron = '<li class="page_next"><a href="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)>0:
        url=urlparse.urljoin("http://es.pornhub.com",matches[0])
        itemlist.append( Item(channel=__channel__, action="buscar", title="Página siguiente >" ,fanart=__fanart__, url=url)) 
    return itemlist



def play(item):
    logger.info("[pornhub.py] play")
    itemlist=[]   
    # Descarga la página
    data = scrapertools.downloadpage(item.url)
    data = scrapertools.unescape(data)
    data = scrapertools.find_single_match(data,'html5Config([^}]+)},')
    url = scrapertools.get_match(data,"src\s+:\s+'([^']+)',")
    item.server="Directo"
    item.url=url
    item.folder=False
    itemlist.append(item)

    return itemlist

