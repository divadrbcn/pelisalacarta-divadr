# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import config
import logger
from core import config
from core.item import Item
 

class DialogoProgreso(object):
  Progreso=""
  Titulo=""
  Closed=False
  def __init__(self, Progreso, Titulo):
    self.Progreso = Progreso
    self.Titulo = Titulo
    self.Closed = False
  def IsCanceled(self):
    from platformcode import cliente
    return self.Progreso.ProgresoIsCanceled()
  
  def Actualizar(self,Porcentaje, Texto):
    from platformcode import cliente
    self.Progreso.ProgresoActualizar(self.Titulo,Texto,Porcentaje)
  
  def Cerrar(self):
    from platformcode import cliente
    self.Progreso.ProgresoCerrar()


def isPlaying():
    from platformcode import cliente
    return cliente.Acciones().isPlaying()
    
    
def Dialog_Progress(title, Texto):
    from platformcode import cliente
    progreso = cliente.Dialogo().ProgresoAbrir(title,Texto,0)
    Progreso = DialogoProgreso(progreso,title)
    return Progreso
    


def Dialog_OK(title, text):
    from platformcode import cliente
    cliente.Dialogo().MostrarOK(title,text)

def Dialog_YesNo(title, text):
    from platformcode import cliente
    return cliente.Dialogo().MostrarSiNo(title,text)
    
def Dialog_Select(title, opciones):
    from platformcode import cliente
    resultado = cliente.Dialogo().Select(title,opciones)
    if resultado ==-1: resultado = None
    return resultado

def AddItem(item, titulo, thumbnail, mode): #----------------------------------OK
#Añade información adicional al title.  
    contextCommands=[]   
    if "," in item.context:
      for menuitem in item.context.split("|"):
        if "," in menuitem:
          from copy import deepcopy
          Menu = deepcopy(item)
          if len(menuitem.split(",")) == 2:
            Titulo = menuitem.split(",")[0]
            Menu.action = menuitem.split(",")[1]
          elif len(menuitem.split(",")) == 3:
            Titulo = menuitem.split(",")[0]
            Menu.channel = menuitem.split(",")[1]
            Menu.action =menuitem.split(",")[2]
          Menu.refered_action = item.action
          contextCommands.append([Titulo,ConstruirURL(Menu)])
    from platformcode import cliente
    cliente.Acciones().AddItem(titulo,thumbnail,item.fanart,item.plot, item.serialize(),contextCommands, mode, item.action)
      

def CloseDirectory(refereditem): #----------------------------------OK
    from platformcode import cliente
    cliente.Acciones().EndItems()
    
    
    
def Refresh(): #----------------------------------OK
    from platformcode import cliente
    cliente.Acciones().Refrescar()
    
def Keyboard(Texto, Title="", Password=False): #----------------------------------OK
    from platformcode import cliente  
    retorno = cliente.Dialogo().MostrarTeclado(Texto, Title, Password) 
    if retorno <>"-1": 
      return retorno
    else:
      return None
    
    
    
def play(item, ItemVideo):
    if not ItemVideo == None:
      from platformcode import cliente  
      url = ItemVideo.url[1]
      cliente.Acciones().Play(item.title, item.plot, url, item.url)
          
def Update(item):
    from platformcode import cliente  
    cliente.Acciones().Update(ConstruirURL(item))

def UpdateLibrary(item):
    pass
    
def ConstruirURL(item):
    return "?" + item.serialize()
    
def ConstruirStrm(item):
    return "?" + item.serialize()
