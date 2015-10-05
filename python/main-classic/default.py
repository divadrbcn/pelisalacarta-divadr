# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC entry point
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# Constants
__plugin__  = "pelisalacarta"
__author__  = "pelisalacarta"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/"
__date__ = "26/03/2015"
__version__ = "4.0"

import os
import sys
from core import config
from core import logger
from core import guitools
import navigation

logger.info("Pelisalacarta init...")

librerias = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'lib' ) )
sys.path.append (librerias)
try:
  config.verify_directories_created()
  itemlist=[]
  item = guitools.ExtraerItem()

  itemlist = navigation.NextItem(item)
  if type(itemlist)==list: 
    if len(itemlist) >0:
      for x in range(len(itemlist)):
        nitem, title, thumbnail = navigation.ItemInfo(item, itemlist[x], 2)
        guitools.AddItem(nitem, title, thumbnail, 2)        
      guitools.CloseDirectory(item)

except:
  import traceback
  logger.error(traceback.format_exc())
  raise Exception('Error en pelisalacarta, comprueba el log')
