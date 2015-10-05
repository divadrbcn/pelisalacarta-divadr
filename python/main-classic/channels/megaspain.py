﻿# -*- coding: utf-8 -*-#------------------------------------------------------------# pelisalacarta - XBMC Plugin# Canal para megaspain# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/#------------------------------------------------------------import urlparse,urllib2,urllib,reimport osimport sysfrom core import loggerfrom core import configfrom core import scrapertoolsfrom core.item import Itemfrom servers import servertools__channel__ = "megaspain"__category__ = "F"__type__ = "generic"__title__ = "Megaspain"__language__ = "ES"__adult__ = "true"DEBUG = config.get_setting("debug")MAIN_HEADERS = []MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )MAIN_HEADERS.append( ["Accept-Encoding","gzip, deflate"] )MAIN_HEADERS.append( ["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"] )MAIN_HEADERS.append( ["Connection","keep-alive"] )MAIN_HEADERS.append( ["DNT","1"] )MAIN_HEADERS.append( ["Referer","http://www.mega-nation.com/index.php"] )MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Windows NT 6.2; rv:18.0) Gecko/20100101 Firefox/18.0"] )MAIN_HEADERS.append( ["Accept-Charset","ISO-8859-1"] )def isGeneric():    return Truedef login():    logger.info("[megaspain.py] login")    # Calcula el hash del password    LOGIN = config.get_setting("megaspainuser")     PASSWORD = config.get_setting("megaspainpassword")    logger.info("LOGIN="+LOGIN)    logger.info("PASSWORD="+PASSWORD)    # Hace el submit del login    post = "user="+LOGIN+"&passwrd="+PASSWORD    logger.info("post="+post)    data = scrapertools.cache_page("http://www.mega-nation.com/index.php?action=login2" , post=post, headers=MAIN_HEADERS)    return Truedef mainlist(item):    logger.info("[megaspain.py] mainlist")    itemlist = []    if config.get_setting("megaspainaccount")!="true":        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="" , url="" , folder=False ) )    else:        if login():            itemlist.append( Item( channel=__channel__ , title="Películas" , action="foro" , url="http://www.mega-nation.com/index.php/board,1.0.html" , folder=True ) )            itemlist.append( Item( channel=__channel__ , title="Series" , action="foro" , url="http://www.mega-nation.com/index.php/board,3.0.html" , folder=True ) )            itemlist.append( Item( channel=__channel__ , title="Documentales" , action="foro" , url="http://www.mega-nation.com/index.php/board,24.0.html" , folder=True ) )            itemlist.append( Item( channel=__channel__ , title="Series Manga/Anime" , action="foro" , url="http://www.mega-nation.com/index.php/board,63.0.html" , folder=True ) )            itemlist.append( Item( channel=__channel__ , title="Peliculas Manga/Anime" , action="foro" , url="http://www.mega-nation.com/index.php/board,64.0.html" , folder=True ) )			            itemlist.append( Item( channel=__channel__ , title="Buscador * Cada palabra debe tener al menos dos caracteres" , action="search" , url="" , folder=True ) )						        else:            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )    return itemlist		def search(item,texto):    logger.info("[megaspain.py] search" + texto)    regexp = "\\+\w\\+"    m1  = re.match(regexp,texto)    logger.info("[megaspain.py] UN SOLO CARACTER EN search" + repr(m1) + " [texto es: " + texto)    item.url = "http://www.mega-nation.com/index.php?action=search2;advanced;sort=id_msg|asc;show_complete=0;searchtype=1;search=%s" % texto    itemlist=[]    data = scrapertools.cache_page(item.url)	#<h5><a href="http://www.mega-nation.com/index.php/board,25.0.html">General</a> / <a href="http://www.mega-nation.com/index.php/topic,163.msg347.html#msg347">El cómico, actor e imitador Dani Martínez se incorpora al elenco de 'Aída</a></h5>	#         <h5><a href="[^"]+">([^<])+</a> / <a href="([^"]+)"><strong class="highlight">Pacific</strong> <strong class="highlight">Rim</strong> (2013) [TS-SCREENER][Castellano MiC HQ][Acción]1,50GB (09/08/2013)</a></h5>	    patron = '<h5><a href="[^"]+">([^<]+)</a> / <a href="([^"]+)">(.*?)</a></h5>'	    matches = re.compile(patron,re.DOTALL).findall(data)    for scrapedforum,scrapedurl, scrapedtitle in matches:            url = urlparse.urljoin(item.url,scrapedurl)            scrapedtitle = scrapedtitle.replace('<strong class="highlight"','')            scrapedtitle = scrapedtitle.replace('</strong>','')            scrapedtitle = scrapedtitle.replace('>','')            scrapedtitle = "[ "+scrapedforum+"] "+scrapedtitle            scrapedtitle = scrapertools.htmlclean(scrapedtitle)            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")            title = scrapedtitle            thumbnail = ""            plot = ""            # Añade al listado            itemlist.append( Item(channel=__channel__, action="findvideos", title= "Subforo " + title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )    return itemlist				def foro(item):    logger.info("[megaspain.py] foro")    itemlist=[]    data = scrapertools.cache_page(item.url)		#EXTRAE SUBFOROS    patron = '<a class="subject" href="([^"]+)" name="[^"]+">([^<]+)</a>' # HAY SUBFOROS    matches = re.compile(patron,re.DOTALL).findall(data)    for scrapedurl,scrapedtitle in matches:                        url = urlparse.urljoin(item.url,scrapedurl)            scrapedtitle = scrapertools.htmlclean(scrapedtitle)            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")            title = scrapedtitle            thumbnail = ""            plot = ""            # Añade al listado            itemlist.append( Item(channel=__channel__, action="foro", title= "Subforo " + title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )    	    #EXTRAE POST	    patron = '\s<span id="([^"]+)"><a href="([^"]+)">([^<]+)</a> </span>' # MANDA A SACAR EL LINK DEL VIDEO    matches = re.compile(patron,re.DOTALL).findall(data)    for scrapedmsg, scrapedurl,scrapedtitle in matches:            scrapedmsg = scrapedmsg.replace("msg_",";msg=")            url = urlparse.urljoin(item.url,scrapedurl)            scrapedtitle = scrapertools.htmlclean(scrapedtitle)            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")            title = scrapedtitle            thumbnail = ""            plot = scrapedmsg            # Añade al listado            itemlist.append( Item(channel=__channel__, action="findvideos", title= title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )			      # EXTREA EL LINK DE LA SIGUIENTE PAGINA    patron = 'div class="pagelinks floatleft.*?<strong>[^<]+</strong>\] <a class="navPages" href="(?!\#bot)([^"]+)">'    matches = re.compile(patron,re.DOTALL).findall(data)    for match in matches:        if len(matches) > 0:            url = match            title = ">> Página Siguiente"            thumbnail = ""            plot = ""            # Añade al listado            itemlist.append( Item(channel=__channel__, action="foro", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )    return itemlistdef findvideos(item):  #show = item.title.replace("Añadir esta serie a la biblioteca de XBMC","")  #logger.info("[megaspain.py] findvideos show "+ show)  itemlist=[]  data = scrapertools.cache_page(item.url)     if 'thank_you_button'in data:    item.url = item.url.replace("php?topic=","php?action=thankyou;topic=")    item.url = item.url + item.plot    data = scrapertools.cache_page(item.url)		  if 'MegaSpain' in data:    patronimage = '<div class="inner" id="msg_\d{1,9}".*?<img src="([^"]+)".*?mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+'    matches = re.compile(patronimage,re.DOTALL).findall(data)    if len(matches)>0:      thumbnail = matches[0]      thumbnail = scrapertools.htmlclean(thumbnail)      thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")      item.thumbnail = thumbnail     patronplot = '<div class="inner" id="msg_\d{1,9}".*?<img src="[^"]+"[^/]+/>(.*?)lgf_facebook_share'    matches = re.compile(patronplot,re.DOTALL).findall(data)    if len(matches)>0:     plot = matches[0]     title = item.title     plot = re.sub('&nbsp;', '', plot)     plot = re.sub('\s\s', '', plot)     plot = scrapertools.htmlclean(plot)     item.plot = ""       from servers import servertools    itemlist.extend(servertools.find_video_items(data=data))    for videoitem in itemlist:     videoitem.channel=__channel__     videoitem.action="play"     videoitem.folder=False     videoitem.thumbnail=item.thumbnail     videoitem.plot = item.plot          videoitem.title = "["+videoitem.server+videoitem.title + " " + item.title     #videoitem.show = show   # if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):   #    itemlist.append( Item(channel=item.channel, title=show + " Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="findvideos") )    return itemlist     else:    item.thumbnail = ""    item.plot = ""    from servers import servertools    itemlist.extend(servertools.find_video_items(data=data))    for videoitem in itemlist:     videoitem.channel=__channel__     videoitem.action="play"     videoitem.folder=False     videoitem.thumbnail=item.thumbnail     videoitem.plot = item.plot     videoitem.title = "["+videoitem.server+videoitem.title + " " + item.title    return itemlist  def test():    # Navega hasta la lista de películas    mainlist_items = mainlist(Item())    menupeliculas_items = menupeliculas(mainlist_items[0])    peliculas_items = peliculas(menupeliculas_items[0])    # Si encuentra algún enlace, lo da por bueno    for pelicula_item in peliculas_items:        itemlist = findbitly_link(pelicula_item)        if not itemlist is None and len(itemlist)>=0:            return True    return False    