# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# XBMC services
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from threading import Thread

def Updater():
  from core import channel_updater
  channel_updater.Check()

def ClearLog():
  from core import config
  import os
  open(os.path.join(config.get_data_path(),"pelisalacarta.log"),"w").write("")

Thread(target=Updater).start() 
Thread(target=ClearLog).start() 