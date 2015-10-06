# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
from core import config
from core import logger
from core import updater
from core.item import Item
import urlparse
from core import scrapertools
import re

def mainlist(item,preferred_thumb=""):
    logger.info(sys._getframe().f_code.co_name)
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]

    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30130) , channel="novedades" , action="mainlist", thumbnail = "%sthumb_novedades.png" ) )
    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes", thumbnail = "%sthumb_canales.png" ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = "%sthumb_buscar.png") )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = "%sthumb_favoritos.png") )
    itemlist.append( Item(title=config.get_localized_string(30131) , channel="biblioteca" , action="mainlist", thumbnail = "%sthumb_biblioteca.png") )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = "%sthumb_descargas.png") )
    itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = "%sthumb_configuracion.png", folder=False) )
    if config.PLATFORM_NAME!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = "%sthumb_ayuda.png") )
    return itemlist


def channeltypes(item, preferred_thumb=""):
    logger.info(sys._getframe().f_code.co_name)
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail="%sthumb_canales_todos"))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail="%sthumb_canales_peliculas"))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail="%sthumb_canales_series"))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail="%sthumb_canales_anime"))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail="%sthumb_canales_documentales"))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail="%sthumb_canales_vos"))
    #itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail="%sthumb_canales_musica"))
    itemlist.append( Item( title="Bittorrent" , channel="channelselector" , action="listchannels" , category="T"   , thumbnail="%sthumb_canales_torrent"))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="L"   , thumbnail="%sthumb_canales_latino"))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="X"   , thumbnail="%sthumb_canales_adultos"))
    #itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail="%sthumb_canales_servidores"))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail="%snovedades"))
    return itemlist
    
def listchannels(item):
    itemlist = []
    try:
        idioma = config.get_setting("languagefilter")
        logger.info("channelselector.filterchannels idioma=%s" % idioma)
        langlistv = ["","ES","EN","IT","PT"]
        idiomav = langlistv[int(idioma)]
        logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
    except:
        idiomav=""

    folderchannels =  []
    disabledchannels =  []
    channelslist =[]
    hiddenchannels = ["__init__.py","ayuda.py", "buscador.py","novedades.py"]
    
    for channel in os.listdir(os.path.join(config.get_runtime_path(),"channels")):
      if channel.endswith(".py") and not channel in  hiddenchannels:
          try:
            exec "from channels import " + channel.replace(".py","") + " as channelmodule"
          except:
            continue
          
          #Crea las propiedades por defecto en caso de que no existan
          if not hasattr(channelmodule,"__channel__"): channelmodule.__channel__ = channel.replace(".py","")
          if not hasattr(channelmodule,"__active__"): channelmodule.__active__ = True
          if not hasattr(channelmodule,"__adult__"): channelmodule.__adult__ = False
          if not hasattr(channelmodule,"__title__"): channelmodule.__title__ = channelmodule.__channel__
          if not hasattr(channelmodule,"__language__"): channelmodule.__language__ = ""
          if not hasattr(channelmodule,"__category__"): channelmodule.__category__ = "*"
          if not hasattr(channelmodule,"__thumbnail__"): channelmodule.__thumbnail__ = ""
          if not hasattr(channelmodule,"__fanart__"): channelmodule.__fanart__ = ""
          if not hasattr(channelmodule,"__type__"): channelmodule.__type__ = "generic"
          

          
          if not channelmodule.__active__:  continue
          if channelmodule.__adult__ and not config.get_setting("enableadultmode") == "true": continue
          if not item.category=="*" and not item.category in channelmodule.__category__: continue
          if not channelmodule.__language__=="" and not idiomav=="" and not idiomav in channelmodule.__language__: continue
          
          if channelmodule.__channel__=="tengourl":
            channelslist.append(Item(title=channelmodule.__title__, channel=channelmodule.__channel__, action="mainlist", thumbnail=channelmodule.__thumbnail__ , fanart=channelmodule.__fanart__ , type=channelmodule.__type__, category=channelmodule.__category__, language=channelmodule.__language__ ))
          else:
            folderchannels.append(Item(title=channelmodule.__title__, channel=channelmodule.__channel__, action="mainlist", thumbnail=channelmodule.__thumbnail__ , fanart=channelmodule.__fanart__ , type=channelmodule.__type__,  category=channelmodule.__category__, language=channelmodule.__language__ ))
                    
    if config.get_setting("personalchannel")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname") ,action="mainlist", channel="personal" ,thumbnail=config.get_setting("personalchannellogo"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname2") ,action="mainlist", channel="personal2" ,thumbnail=config.get_setting("personalchannellogo2"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname3") ,action="mainlist", channel="personal3" ,thumbnail=config.get_setting("personalchannellogo3"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname4") ,action="mainlist", channel="personal4" ,thumbnail=config.get_setting("personalchannellogo4"), language="" , category="F,S,D,A" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        channelslist.append( Item( title=config.get_setting("personalchannelname5") ,action="mainlist", channel="personal5" ,thumbnail=config.get_setting("personalchannellogo5"), language="" , category="F,S,D,A" , type="generic"  ))

    folderchannels.sort(key=lambda item: item.title.lower().strip())
    channelslist.extend(folderchannels)

    for channel in channelslist:
        if channel.thumbnail == "": channel.thumbnail = "%s"+channel.channel+".png"
        itemlist.append(channel)

    return itemlist

