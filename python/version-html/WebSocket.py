# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# HTTPServer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import sys
import os
from core import logger
from core import config
from threading import Thread
import WebSocketServer

MostrarInfo= None
ProcessRequest = None
data = open(os.path.join(config.get_runtime_path(),"version.xml"),"r").read()
version = data.split("<tag>")[1].split("</tag>")[0]
fecha = data.split("<date>")[1].split("</date>")[0]

class HandleWebSocket(WebSocketServer.WebSocket):
   def handleMessage(self):
      if self.data is None: self.data = ''
      
      if str(self.data).startswith("?"):
        sys.argv[str(self)]["Request"]=str(self.data).replace("?","")
        global ProcessRequest
        Thread(target=ProcessRequest,args=[self]).start()  
                 
      elif str(self.data).startswith("!"):
        sys.argv[str(self)]["Data"]=str(self.data).replace("!","")
      

   def handleConnected(self):
      sys.argv[str(self)]={"Socket": self, "Request":"", "Data":"","Host":""}
      self.sendMessage('{"Action": "Connect", "Version": "pelisalacarta '+version+'", "Date":"'+fecha+'"}')
      global MostrarInfo
      MostrarInfo()

   def handleClose(self):
    if str(self) in sys.argv:
      del sys.argv[str(self)]
      global MostrarInfo
      MostrarInfo()



WebsocketPort=int(config.get_setting("websocket.port"))
server = WebSocketServer.SimpleWebSocketServer("",WebsocketPort,HandleWebSocket)

def start(Request, Info):
    global ProcessRequest
    global MostrarInfo
    ProcessRequest=Request
    MostrarInfo = Info
    Thread(target=server.serveforever).start()
 
def stop():
    server.close()
