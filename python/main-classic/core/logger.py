# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Logger para XBMC (Propio)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import logging.config
import logging
import config

class ExtendedLogger(logging.Logger):
    def findCaller(self):
        f = logging.currentframe().f_back.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if "logger" in filename: # This line is modified.
                f = f.f_back
                continue
            if co.co_name == "<module>":
              rv = (filename , f.f_lineno, co.co_name)
            else:
              rv = (filename + " [" + co.co_name + "]" , f.f_lineno, co.co_name)
            break
        return rv

logging.setLoggerClass(ExtendedLogger)        
logging.basicConfig(level=logging.DEBUG,
format='%(levelname)-5s  %(asctime)s  %(filename)-40s  %(message)s',
datefmt="%d/%m/%y-%H:%M:%S",
filename=os.path.join(config.get_data_path(),"pelisalacarta.log"),
filemode='a')
logger_object=logging.getLogger("kodi")

def info(texto):
  if int(config.get_setting("debuglevel")) >= 3:
      logger_object.info(unicode(str(texto),"utf-8","ignore").replace("\n","\n"+ " "*68))

def debug(texto):
  if int(config.get_setting("debuglevel")) >= 2:
      logger_object.debug(unicode(str(texto),"utf-8","ignore").replace("\n","\n"+ " "*68))

def error(texto):
  if int(config.get_setting("debuglevel")) >= 1:
    logger_object.error(unicode(str(texto),"utf-8","ignore").replace("\n","\n"+ " "*68))
