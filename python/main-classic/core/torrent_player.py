# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# cliente torrent para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import time
import guitools
from core import scrapertools
from core import config
from core import logger
from core.item import Item
import bencode

__module__ = "Torrent"


def download(item, VideoItem=Item(url=["",""]), Reproducir =  False):
    logger.info("[torrent_player.py] - play")
    try:
      PorcentajeInicio = int(config.get_setting("porcentaje_torrent"))
    except:
      PorcentajeInicio = 5
      
    video_file_path = ""
    video_file = ""
    video_file_size = 0
    Cancelado = False

    #importa la libreria si no la encuentra sale de la funcion
    lt = libtorrent()
    if lt is None:
      return -2
      
    #Para enlaces de EliteTorrent y quiza otros
    import HTMLParser
    item.url =  HTMLParser.HTMLParser().unescape(item.url)
    
    
    #Creamos el directorio
    save_path_videos = os.path.join( config.get_setting("downloadpath") , "Torrent")
    if not os.path.exists(save_path_videos): os.mkdir(save_path_videos)
    
    #Creamos la sesion
    session = lt.session()
    settings = session.settings()
    settings.stop_tracker_timeout = 5
    session.set_settings(settings)
    session.stop_dht()
    session.listen_on(0,0)
    session.add_dht_router("router.bittorrent.com",6881)
    session.add_dht_router("router.utorrent.com",6881)
    session.add_dht_router("router.bitcomet.com",554)
    session.start_dht(None)    

    #Añadimos el torrent
    if not item.url.startswith("magnet:" ):
      if os.path.isfile(item.url):
        f = open(url,'rb')
        data = f.read()
        info = lt.torrent_info(bencode.bdecode(data))
        f.close()
      else:
        data = scrapertools.downloadpage(item.url, addheaders=[["Referer",item.url]])
        info = lt.torrent_info(bencode.bdecode(data))
      
      torrent = session.add_torrent({'ti':info     , 'save_path':save_path_videos, 'storage_mode':lt.storage_mode_t.storage_mode_allocate})
    else:
      torrent = session.add_torrent({'url':item.url, 'save_path':save_path_videos, 'storage_mode':lt.storage_mode_t.storage_mode_allocate})

    #Descarga secuencial
    torrent.set_sequential_download(True)

    Time = time.time()
    pDialog = guitools.Dialog_Progress(__module__,"Iniciando descarga...")
    
    #Esperamos a los metadatos
    while not torrent.has_metadata():
      time.sleep(1)
      if pDialog.IsCanceled():
          pDialog.Cerrar()
          Cancelado =True
          break
      Progreso(session,torrent,pDialog,Time,0)
      
    #Obtenemos la info del Torrent
    if torrent.has_metadata():
      info = torrent.get_torrent_info()
      VideoFiles=[]
      SrtFiles=[]
      Files = []
      for f in info.files():
        Size = 0
        for file in Files:
          Size += file["Size"]

        Start = int(Size / info.piece_length())
        End = int((Size + f.size) / info.piece_length()) 
        Files.append({"Start":Start, "End" : End, "Size": f.size, "Path" : f.path})
        
        
      VideoExtensions =  ["avi", "mp4", "mkv", "flv", "mpeg", "ts"]  
      
      for file in Files:
        if file["Path"].split(".")[len( file["Path"].split("."))-1].lower() in VideoExtensions:
          VideoFiles.append(file)

        elif file["Path"].split(".")[len(file["Path"].split("."))-1].lower() =="srt":
         SrtFiles.append(file)

          
      VideoItem.url[1] = os.path.join(save_path_videos, VideoFiles[0]["Path"].encode("utf8"))
      
      
      #Loop para controlar la descarga
      ReproduccionIniciada = False
      IniciarAutomatico = Reproducir
      
      while (not torrent.is_seed()):
          time.sleep(1)
          VideoFile = VideoFiles[0]
          PiezaLista = VideoFile["Start"]
          for x in range(VideoFile["Start"],VideoFile["End"]- VideoFile["Start"] +1):
            if torrent.status().pieces[x]: 
              PiezaLista = x
            else:
              break
              


          #Los Srt Primero      
          if len(SrtFiles):
            SrtFile = SrtFiles[0]
            for x in range(SrtFile["Start"],SrtFile["End"]- SrtFile["Start"] +1):
              torrent.piece_priority(x,7)
          Progreso(session,torrent,pDialog,Time,PiezaLista)
          
          #Si se cierra el reproductor, vuelve a mostrar el progreso
          if not guitools.isPlaying() and ReproduccionIniciada:
            ReproduccionIniciada = False
            IniciarAutomatico = False
            pDialog = guitools.Dialog_Progress(__module__,"")
            Progreso(session,torrent,pDialog,Time,PiezaLista)

          #Para cancelar la descarga
          if not guitools.isPlaying() and pDialog.IsCanceled():
            pDialog.Cerrar()
            Respuesta = guitools.Dialog_YesNo(__module__,"Presione 'Si' para cancelar la descarga y 'No' para cerrar el dialogo e iniciar la reproduccion.")
            
            if Respuesta == True:
              Cancelado =True
              break;           
            else:
              ReproduccionIniciada =True
              guitools.play(item,VideoItem)
              
              
           
          #Para reproducir el vídeo    
          if torrent.status().state ==3 and  (torrent.status().progress * 100) >= PorcentajeInicio and not guitools.isPlaying() and IniciarAutomatico and not ReproduccionIniciada:
            logger.info("[torrent_player.py] - Iniciando reproduccion")
            pDialog.Cerrar()
            ReproduccionIniciada = True
            guitools.play(item,VideoItem)



    #Si llega aqui es porque se ha cancelado o porque la descarga ha terminado.
    #si se esta reprodciendo se espera.
    while guitools.isPlaying():
      time.sleep(1)

    
    #Si era una reproduccion, pregunta si desea eliminar los datos descargados
    if Reproducir:
      pDialog.Cerrar()
      Respuesta = guitools.Dialog_YesNo(__module__,"Eliminar los datos descargados?")
      pDialog = guitools.Dialog_Progress(__module__,"")
      pDialog.Actualizar(25, "Deteniendo Torrent")
      if Respuesta ==True:
        session.remove_torrent(torrent,1)
      else:
        session.remove_torrent(torrent,0)
      pDialog.Actualizar(50, "Eliminando sesion")
      del session
      pDialog.Actualizar(75, "Deteniendo libtorrent")
      del lt
      pDialog.Cerrar()
      if Respuesta ==True:
        guitools.Dialog_OK(__module__, 'Torrent eliminado y datos borrados.')
    
    #Si era una descarga, detiene el torrent.
    else:
      pDialog = guitools.Dialog_Progress(__module__,"")
      pDialog.Actualizar(25, "Deteniendo Torrent")
      session.remove_torrent(torrent,0)
      pDialog.Actualizar(50, "Eliminando sesion")
      del session
      pDialog.Actualizar(75, "Deteniendo libtorrent")
      del lt
      
      #Si la descarga se ha completado, la mueve a la carpeta descargas
      if not Cancelado:
        '''
        RutaArchivo = os.path.join(config.get_setting("downloadpath"),item.title + "." + video_file.split(".")[len(video_file.split("."))-1] )
        if os.path.exists(RutaArchivo):
          os.remove(RutaArchivo)
        if os.path.exists(os.path.join(save_path_videos,video_file_path)):
          os.rename(os.path.join(save_path_videos,video_file_path), RutaArchivo )
          import shutil
          shutil.rmtree(os.path.join(save_path_videos,video_file_path.replace(save_path_videos,"").replace(video_file,"")))
        '''  
        pDialog.Cerrar()
        return 0
        
      else:
        pDialog.Cerrar()
        return -1
     
      


def Progreso(session,torrent,pDialog,Time, PiezaLista):
  s= torrent.status()
  if session.dht_state() is not None:
      DHT=str(session.status().dht_nodes)
  else:
      DHT="inactivo"  

  trackers= 0 

  for tracker in torrent.trackers():
    trackers+=1

  Estados = ['En Cola', 'Comprobando', 'Descargando Metadatos', 'Descargando', 'Finalizado', 'Seeding', 'Allocating', 'Checking fastresume']
  Mensaje  = 'Tiempo: %s Estado: %.1f%% - %s Piezas listas: %i\n'
  Mensaje += 'Descarga:%.1f kb/s Subida:%.1f kB/s \n'
  Mensaje += 'Peers:%d Seeds:%d Nodos DHT:%s Trackers: %i' 

  Mensaje  = Mensaje % (time.strftime("%H:%M:%S", time.gmtime(time.time() - Time)),s.progress * 100, Estados[s.state], PiezaLista, s.download_rate / 1000, s.upload_rate / 1000,s.num_peers, s.num_seeds,DHT,trackers)
  Progreso = int(s.progress * 100)
  pDialog.Actualizar(Progreso, Mensaje)
  
def libtorrent():
  try:
  
    import libtorrent as lt
    if not lt.version in ["0.14.10.0","0.16.10.0", "0.15.10.0", "0.16.18.0"]:
        guitools.Dialog_OK("Torrent","La versión de libtorrent instalada es: " + lt.version + "\nNo se garantiza su funcionamento con esta versión")

  except (ImportError): 
    guitools.Dialog_OK("Error","No se ha podido localizar la libreria libtorrent, asegurate de que la tienes instalada correctamente.")
    return None
  return lt
