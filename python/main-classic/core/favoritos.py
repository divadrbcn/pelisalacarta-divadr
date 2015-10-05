# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos favoritos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urllib
import os
import sys
import downloadtools
import config
import logger
import samba
from item import Item

BOOKMARK_PATH = config.get_setting("bookmarkpath")

def mainlist(item):
    logger.info("[favoritos.py] mainlist")
    itemlist=[]

    # Crea un listado con las entradas de favoritos
    if usingsamba(BOOKMARK_PATH):
        ficheros = samba.get_files(BOOKMARK_PATH)
    else:
        ficheros = os.listdir(BOOKMARK_PATH)
    ficheros.sort()
    
    # Rellena el listado
    for fichero in ficheros:
      itemlist.append(LeerFavorito(fichero))
    return itemlist

def LeerFavorito(Nombre,Ruta=BOOKMARK_PATH):
    logger.info("[favoritos.py] LeerFavorito")

    if usingsamba(Ruta):
        Archivo = samba.get_file_handle_for_reading(Nombre, Ruta)
    else:
        Archivo = open(os.path.join(Ruta, Nombre))
        
    JSONItem = Archivo.read()
    Archivo.close();
    item = Item()
    item.fromjson(JSONItem)
    if item.context:
      item.context +="|Eliminar,remove_from_favorites"
    else:
      item.context = "Eliminar,remove_from_favorites"
    
    return item

def GuardarFavorito(item, Ruta=BOOKMARK_PATH):
    logger.info("[favoritos.py] GuardarFavorito")
    import time
    # Lee todos los ficheros
    if usingsamba(Ruta):
        ficheros = samba.get_files(Ruta)
    else:
        ficheros = os.listdir(Ruta)

    filename = str(int(time.time())) + ".json"
    fullfilename = os.path.join(Ruta,filename)
    logger.info("[favoritos.py] savebookmark filename="+filename)
    
    # Genera el contenido
    if item.refered_action: item.action = item.refered_action
    item.context =""
    item.file = fullfilename
    filecontent = item.tojson()

    # Graba el fichero
    import json
    if not usingsamba(Ruta):
        open(fullfilename.decode("utf-8"),"w").write(filecontent)
    else:
        samba.write_file(filename, filecontent, Ruta)

def BorrarFavorito(item,Ruta=BOOKMARK_PATH):
    logger.info("[favoritos.py] BorrarFavorito")

    if not usingsamba(Ruta):
        os.remove(item.file)
    else:
        fullfilename = item.file.replace("\\","/")
        partes = fullfilename.split("/")
        filename = partes[len(partes)-1]
        samba.remove_file(filename,Ruta)

def usingsamba(path):
    return path.upper().startswith("SMB://")
