# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Codificacion de rutas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
def EncodePath(dir):
  encoding=sys.getfilesystemencoding()
  if encoding == "ANSI_X3.4-1968":encoding = "utf8"
  return dir.decode("utf8").encode(encoding)
  
def DecodePath(dir):
  encoding=sys.getfilesystemencoding()
  if encoding == "ANSI_X3.4-1968":encoding = "utf8"
  return dir.decode(encoding).encode("utf8") 