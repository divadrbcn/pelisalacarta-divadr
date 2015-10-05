# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Módulo para acciones en el cliente HTML
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys, os
import json

import threading
import urllib
import base64
from core.config import get_localized_string

ItemList = []

def getThread():
  return threading.current_thread().name
def SendMessage(Data):
  try:
    sys.argv[sys.argv[getThread()]["Socket"]]["Socket"].sendMessage(Data)
  except:
    pass

def GetData():
  try:
    data = sys.argv[sys.argv[getThread()]["Socket"]]["Data"]
  except:
    data = ""
  return data
  
def GetHost():
  try:
    data = sys.argv[sys.argv[getThread()]["Socket"]]["Host"]
  except:
    data = ""
  return data
  
def SetData(Data):
  try:
    sys.argv[sys.argv[getThread()]["Socket"]]["Data"] = Data
  except:
    pass
  
class Dialogo(object):
    
  def ProgresoAbrir(self,Titulo="",Mensaje="", Porcentaje=0):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Progress" 
    JsonData["Title"]=Titulo
    JsonData["Text"]=Mensaje
    JsonData["Progress"]=Porcentaje
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Progress' enviada.")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")

    return self
    
  def ProgresoActualizar(self,Titulo="",Mensaje="",Porcentaje=0):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="ProgressUpdate" 
    JsonData["Title"]=Titulo
    JsonData["Text"]=Mensaje
    JsonData["Progress"]=Porcentaje
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'ProgressUpdate' enviada")
    #while GetData() == None:
      #continue
    ##logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
      
  def ProgresoIsCanceled(self):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="ProgressIsCanceled" 
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'ProgressIsCanceled' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    if GetData() =="true":
      return True
    else:
      return False
    
  def ProgresoCerrar(self):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="ProgressClose" 
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'ProgressClose' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")

  def MostrarOK(self,Titulo="",Mensaje=""):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Alert" 
    JsonData["Title"]=Titulo
    JsonData["Text"]=unicode(Mensaje ,"utf8","ignore").encode("utf8")
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Alert' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    
  def MostrarSiNo(self,Titulo="",Mensaje=""):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="AlertYesNo" 
    JsonData["Title"]=Titulo
    JsonData["Text"]=Mensaje
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'AlertYesNo' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    if GetData() == "yes":
      return True
    else:
      return False
    
  def MostrarTeclado(self,Texto="",Titulo="", Password=False):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Keyboard" 
    JsonData["Title"]=Titulo
    JsonData["Text"]=Texto
    JsonData["Password"]=str(Password)
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Keyboard' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    return GetData()

  def Select(self,Titulo,Elementos=[]):
    SetData(None)
    JsonData = {}
    JsonList={}
    JsonList["Count"]=0
    for Elemento in Elementos:
      JsonList["Title"+str(JsonList["Count"])] = Elemento
      JsonList["Count"]+=1

    JsonData["Action"]="List" 
    JsonData["Title"]=Titulo
    JsonData["List"]=JsonList
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'List' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    if GetData() <> "-1":
      return int(GetData())
    else:
      return None

class Acciones(object):

  def Refrescar(self,Scroll=False):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Refresh" 
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Refresh' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    
  def AddItem(self,Title="",Thumbnail="", Fanart="", Plot="",Url="",ContextMenu=[], Mode=0, Action=""):
    global ItemList
    SetData(None)
    JsonData = {}
    JsonContext={}
    JsonContext["Count"]=0
    for Comando in ContextMenu:
      JsonContext["Title"+str(JsonContext["Count"])] = Comando[0]
      JsonContext["Url"+str(JsonContext["Count"])] = Comando[1]
      JsonContext["Count"]+=1
      
    JsonData["Action"]="AddItem"
    JsonData["Mode"]=Mode    
    JsonData["Title"]=Title
    JsonData["Thumbnail"]= Thumbnail
    JsonData["Fanart"]=Fanart
    JsonData["Plot"]=Plot
    JsonData["ItemAction"]=Action
    JsonData["Url"]=Url
    JsonData["Host"] =  GetHost()
    JsonData["ContextMenu"]=JsonContext
    ItemList.append(JsonData)
    #SendMessage(json.dumps(JsonData))

  def EndItems(self):
    global ItemList
    SetData(None)
    JsonData = {}
    JsonData["Action"]="EndItems" 
    JsonData["Itemlist"]=ItemList
    SendMessage(json.dumps(JsonData))
    ItemList= []
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'EndItems' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    
  def Play(self,Title="",Plot="",Url="", ServerURL=""):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Play" 
    JsonData["Title"]= Title
    JsonData["Plot"]= Plot
    JsonData["Url"] =  Url
    JsonData["ServerUrl"] =  ServerURL
    JsonData["Host"] =  GetHost()
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Play' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")

  def AbrirConfig(self,Opciones):
    from core import config
    SetData(None)
    JsonData = {}
    JsonOpciones={}
    JsonOpciones["Count"]=0
    for Opcion in Opciones:
      try:
        Opcion[0] = get_localized_string(int(Opcion[0]))
      except:
        pass
      try:
        ops = Opcion[3].split("|")
        for x, op in enumerate(ops):
          ops[x] = get_localized_string(int(ops[x])) 
        Opcion[3] = "|".join(ops)
      except:
        pass
      try:
        Opcion[8] = get_localized_string(int(Opcion[8]))
      except:
        pass
      
      JsonOpciones["Label"+str(JsonOpciones["Count"])] = Opcion[0]
      JsonOpciones["Id"+str(JsonOpciones["Count"])] = Opcion[1]
      JsonOpciones["Type"+str(JsonOpciones["Count"])] = Opcion[2]
      JsonOpciones["Lvalues"+str(JsonOpciones["Count"])] = Opcion[3]
      JsonOpciones["Values"+str(JsonOpciones["Count"])] = Opcion[4]
      JsonOpciones["Value"+str(JsonOpciones["Count"])] = Opcion[5]
      JsonOpciones["Option"+str(JsonOpciones["Count"])] = Opcion[6]
      JsonOpciones["Enabled"+str(JsonOpciones["Count"])] = Opcion[7]
      JsonOpciones["Category"+str(JsonOpciones["Count"])] = Opcion[8]
      JsonOpciones["Count"]+=1
      
    JsonData["Action"]="OpenConfig"    
    JsonData["Options"]=JsonOpciones

    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'OpenConfig' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    
    if GetData():
      if GetData() <> "-1":
        JsonRespuesta = json.loads(GetData())
        from core import config
        config.set_settings(JsonRespuesta)
      JsonData = {}
      JsonData["Action"]="HideLoading"
      SendMessage(json.dumps(JsonData))
      
   
 
  def Update(self,url):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="Update" 
    JsonData["Url"]=url
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'Update' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------")
    
    
  def isPlaying(self):
    SetData(None)
    JsonData = {}
    JsonData["Action"]="isPlaying" 
    SendMessage(json.dumps(JsonData))
    #logger.info("-----------------------------------------------------------------------")
    #logger.info("Petición de 'isPlaying' enviada")
    while GetData() == None:
      continue
    #logger.info("Respuesta Recibida: " + GetData())
    #logger.info("-----------------------------------------------------------------------") 
    if GetData() =="true":
      return True
    else:
      return False    
  
    