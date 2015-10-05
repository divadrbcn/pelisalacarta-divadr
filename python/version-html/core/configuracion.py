# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuración
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import downloadtools
from core import config
from core import logger

logger.info("[configuracion.py] init")

def mainlist(item):
    logger.info("[configuracion.py] mainlist")
    
    if config.get_setting("usepassword") =="true":
      import guitools
      password = guitools.Keyboard("", "Escriba la contraseña", True)
      if password == config.get_setting("password"):
        config.open_settings()
      else:
        guitools.Dialog_OK("Error", "La contraseña no es correcta")
    else:
      config.open_settings()
