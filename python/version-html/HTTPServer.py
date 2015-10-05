# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# HTTPServer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import sys
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from core import logger
from core import config
from threading import Thread
import time

class MyHTTPServer(ThreadingMixIn, HTTPServer):
    def handle_error(self, request, client_address):
      import traceback
      if not "Errno 10054" in traceback.format_exc() and not "Errno 10053" in traceback.format_exc():
        logger.error(traceback.format_exc())
      else:
        logger.info( "Conexion Cerrada")
       
class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args): 
      #sys.stderr.write("%s - - [%s] %s\n" %(self.client_address[0], self.log_date_time_string(), format%args))
      pass

    def do_GET(self):     
        try:
            host = self.headers.get("Host")
        except:
            host = ""
        if ":" in host: host = host.split(":")[0]

        #Control de accesos
        Usuario = "user"
        Password = "password"
        ControlAcceso = False
        import base64
        #Comprueba la clave
        if ControlAcceso and self.headers.getheader('Authorization') <> "Basic " + base64.b64encode(Usuario + ":"+ Password):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Introduce el nombre de usuario y clave para acceder a pelisalacarta\"')
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('¡Los datos introducidos no son correctos!')
            return
        
        
        if self.path =="/":
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , "page.html" ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            respuesta = f.read()
            respuesta = respuesta.replace("{$host}","ws://"+host + ":"+config.get_setting("websocket.port")+"/")
            self.wfile.write(respuesta)
            f.close()
      
        elif self.path.startswith("/image-"):
          import urllib2, urllib
          import base64
          url= self.path.replace("/image-","")
          url = base64.b64decode(urllib.unquote_plus(url)) 
          try:
            Headers = self.headers.dict
            if 'host' in Headers.keys(): del Headers["host"]
            if 'referer' in Headers.keys(): del Headers["referer"]
            
            req = urllib2.Request(url, headers=Headers)
            response = urllib2.urlopen(req)
            self.send_response(200)
            self.send_headers=response.info()
            self.end_headers()
            self.wfile.write(response.read())
            self.wfile.close()
            response.close() 
          except:
            self.send_response(400)
            self.wfile.close()
            
        elif self.path.startswith("/local-"):
          import base64
          import urllib
          Path= self.path.replace("/local-","").replace(".mp4","")  
          Path = base64.b64decode(urllib.unquote_plus(Path))
          Size = int(os.path.getsize(Path.decode("utf8") ))
          f=open(Path.decode("utf8") , "rb" )
          if not self.headers.get("range") ==None:
            if "=" in str(self.headers.get("range")) and "-" in str(self.headers.get("range")):
              Inicio= int(self.headers.get("range").split("=")[1].split("-")[0])
              if self.headers.get("range").split("=")[1].split("-")[1]<>"": 
                Fin= int(self.headers.get("range").split("=")[1].split("-")[1])
              else:
                Fin = Size-1
            
          else:
            Inicio=0
            Fin = Size-1
          
          if not Fin > Inicio: Fin = Size-1
            
          if self.headers.get("range") ==None:
            logger.info("-------------------------------------------------------")
            logger.info("Solicitando archivo local: "+ Path)
            logger.info("-------------------------------------------------------")
            
            self.send_response(200)
            self.send_header("Content-Disposition", "attachment; filename=video.mp4")  
            self.send_header('Accept-Ranges', 'bytes')   
            self.send_header('Content-Length', str(Size))   
            self.send_header("Connection", "close") 
            self.end_headers()
            while True:
              time.sleep(0.2)
              buffer =f.read(1024*250)
              if not buffer:
                break
              self.wfile.write(buffer)
            self.wfile.close()
            f.close()
          else:
            logger.info("-------------------------------------------------------")
            logger.info("Solicitando archivo local: "+ Path)
            logger.info("Rango: "+ str(Inicio) + "-" + str(Fin) + "/" + str(Size))
            logger.info("-------------------------------------------------------")
            f.seek(Inicio)
            
            self.send_response(206)
            self.send_header("Content-Disposition", "attachment; filename=video.mp4")  
            self.send_header('Accept-Ranges', 'bytes')   
            self.send_header('Content-Length', str(Fin-Inicio))   
            self.send_header('Content-Range', str(Inicio) + "-" + str(Fin) + "/" + str(Size))
            self.send_header("Connection", "close") 
            
            self.end_headers()
            while True:
              time.sleep(0.2)
              buffer =f.read(1024*250)
              if not buffer:
                break
              self.wfile.write(buffer)
            self.wfile.close()
            f.close()         
            
        elif self.path.startswith("/remote-"):
          import urllib2, urllib
          url= self.path.replace("/remote-","").replace(".mp4","")
          import base64
          url = base64.b64decode(urllib.unquote_plus(url))
          Headers = self.headers.dict
          h=urllib2.HTTPHandler(debuglevel=0)
          request = urllib2.Request(url)
          request.add_header("Accept-Encoding","")
          for header in Headers:
            if not header in ["host","referer","user-agent"]:
              request.add_header(header,Headers[header])
            
          opener = urllib2.build_opener(h)
          urllib2.install_opener(opener)  
          connexion = opener.open(request)
          self.send_response(connexion.getcode())
          ResponseHeaders = connexion.info()
          logger.info("------------------------------------")
          logger.info(url)
          logger.info(connexion.getcode())
          logger.info("Headers:")
          for header in ResponseHeaders:
            if header in ["content-disposition"]:
              logger.info("Eliminado Header ->" + header + "=" + ResponseHeaders[header])
            
            else:
              self.send_header(header, ResponseHeaders[header])
              logger.info("Reenviado Header ->" + header + "=" + ResponseHeaders[header])
          logger.info("Añadido Header   ->" + "content-disposition" + "=" + "attachment; filename=video.mp4")
          self.send_header("content-disposition", "attachment; filename=video.mp4")    
          self.end_headers()
          blocksize = 1024
          bloqueleido = connexion.read(blocksize)
          while len(bloqueleido)>0:
            self.wfile.write(bloqueleido)
            bloqueleido = connexion.read(blocksize)
          logger.info("Terminado")
          logger.info("------------------------------------")
          self.wfile.close()
          connexion.close()
             
        elif self.path.startswith("/netutv-"):
          import urllib2, urllib
          url= self.path.replace("/netutv-","").replace(".mp4","")
          import base64
          url = base64.b64decode(urllib.unquote_plus(url))
          Headers = self.headers.dict
          h=urllib2.HTTPHandler(debuglevel=0)
          request = urllib2.Request(url)
          request.add_header("Accept-Encoding","")
          for header in Headers:
            if not header in ["host","user-agent"]:
              request.add_header(header,Headers[header])
            
          opener = urllib2.build_opener(h)
          urllib2.install_opener(opener)  
          connexion = opener.open(request)
          self.send_response(connexion.getcode())
          ResponseHeaders = connexion.info()
          logger.info("------------------------------------")
          logger.info(url)
          logger.info(connexion.getcode())
          logger.info("Headers:")
          for header in ResponseHeaders:
              self.send_header(header, ResponseHeaders[header])
              logger.info("Reenviado Header ->" + header + "=" + ResponseHeaders[header])

          self.end_headers()

          if url.endswith(".m3u8"):
            m3u8 = connexion.read()
            base = url.replace(url.split("/")[len(url.split("/"))-1],"")
            file = url.replace(base,"").replace(".m3u8","")
            import re
            patron="("+file+"[^\.]+\.ts)"
            matches = re.compile(patron,re.DOTALL).findall(m3u8)
            for video in matches:
              m3u8 = m3u8.replace(video,"netutv-"+urllib.quote_plus(base64.b64encode(base+video))+".mp4")
            self.wfile.write(m3u8)
            self.wfile.close()
            connexion.close()
            logger.info("Terminado")
            logger.info("------------------------------------")
          
          else:
            blocksize = 1024
            bloqueleido = connexion.read(blocksize)
            while len(bloqueleido)>0:
              self.wfile.write(bloqueleido)
              bloqueleido = connexion.read(blocksize)
            logger.info("Terminado")
            logger.info("------------------------------------")
            self.wfile.close()
            connexion.close()
             
        elif self.path.endswith(".jpg"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".png"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            
        elif self.path.endswith(".gif"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            
        elif self.path.endswith(".css"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".js"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith(".html"):
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        else:
            f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , self.path[1:] ), "rb" )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        return
    
    def address_string(self):
        # Disable reverse name lookups
        return self.client_address[:2][0] 
        
PORT=int(config.get_setting("server.port"))
server = MyHTTPServer(('', PORT), Handler)  

def start():
    Thread(target=server.serve_forever).start()
 
def stop():
    server.socket.close()
    server.shutdown()
    