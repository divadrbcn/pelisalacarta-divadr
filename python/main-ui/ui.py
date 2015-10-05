# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# KODI Ui interface
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
import sys
import urlparse,urllib,urllib2
import xbmc
import xbmcgui
import xbmcaddon
from core.item import Item
from core import logger
from core import config
import navigation


ACTION_MOVE_LEFT       =  1 #Dpad Left
ACTION_MOVE_RIGHT      =  2 #Dpad Right
ACTION_MOVE_UP         =  3 #Dpad Up
ACTION_MOVE_DOWN       =  4 #Dpad Down
ACTION_PAGE_UP         =  5 #Left trigger
ACTION_PAGE_DOWN       =  6 #Right trigger
ACTION_SELECT_ITEM     =  7 #'A'
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9 #'B'
ACTION_PREVIOUS_MENU   = 10 #'Back'
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13 #'Start'
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15
ACTION_XBUTTON         = 18 #'X'
ACTION_YBUTTON         = 34 #'Y'
ACTION_MOUSEMOVE       = 90 # Mouse has moved
ACTION_MOUSEMOVE2      = 107 # Mouse has moved
ACTION_PREVIOUS_MENU2  = 92 #'Back'
ACTION_CONTEXT_MENU    = 117 # pops up the context menu
ACTION_CONTEXT_MENU2   = 229 # pops up the context menu (remote control "title" button)


WindowXMLDialog = None
WindowXML = None


def WindowDialog(title, Texto,percent):
  global WindowXMLDialog
  if not WindowXMLDialog== None:
    WindowXMLDialog.close()
    WindowXMLDialog = None
  from threading import Thread
  Thread(target=ProgressWindowT, args=[title, Texto,percent]).start()
  while WindowXMLDialog == None:
    pass
  return WindowXMLDialog

def ProgressWindowT(title, Texto,percent):
  ProgressWindow("ProgressDialog.xml",config.get_runtime_path()).show(title, Texto,percent)

class ProgressWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_name, fallback_path):
        self.canceled = False
        global WindowXMLDialog
        WindowXMLDialog=self
        
    def show(self,title, text, percent=0):
        self.text = text
        self.title = title
        self.percent = percent
        self.doModal()
       
    def isCanceled(self):
        return self.canceled
           
    def update(self, text, percent):
        self.text = text
        self.percent = percent
        self.onInit()
        
    def onInit(self): 
        title = self.title
        if self.percent > 0: title += ": " + str(self.percent) + "%"
        if self.canceled: title += " - Cancelando..."
        self.getControl(12).setLabel(title)
        self.getControl(131).setLabel(self.text)
        if self.percent ==0:
          self.getControl(133).setWidth(0)
        else:
          self.getControl(133).setWidth((self.percent * (self.getControl(132).getWidth()-4))/100)
        self.setFocusId(134)
        self.started = True
         
    def onAction(self, action):
      pass
      
    def onClick( self, control_id ):
      if control_id == 134 or control_id == 11:
        self.canceled = True
        self.onInit()
      if control_id == 11:
        self.close()


class OKWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_name, fallback_path):
        pass
        
    def show(self,title, text):
        self.text = text
        self.title =  title
        self.doModal() 
        
    def onInit(self):   
        self.getControl(12).setLabel(self.title)
        self.getControl(131).setLabel(self.text)
        self.setFocusId(132)

    def onAction(self, action):
      pass
      
    def onClick(self, control_id):
      if control_id == 132:
        self.close()
      if control_id == 11:  
        self.close()

class YesNoWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_name, fallback_path):
        self.result = None
        
    def show(self,title, text):
        self.text = text
        self.title =  title
        self.doModal()
        return self.result 
        
    def onInit(self):   
        self.getControl(12).setLabel(self.title)
        self.getControl(131).setLabel(self.text)
        self.setFocusId(133)

    def onAction(self, action):
      pass
      
    def onClick(self, control_id):
      if control_id == 132:
        self.result = True
        self.close()
      if control_id == 133:
        self.result = False
        self.close()        
      if control_id == 11:
        self.result = False
        self.close()
        
class SelectWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_name, fallback_path):
        self.result = -1
        
    def setOptions(self,title, options):
        self.options = options
        self.title =  title
        self.doModal() 
        return self.result
        
    def onInit(self):
        px = (6 - len(self.options))*43
        if px > 0:
          self.getControl(10041).setHeight(self.getControl(10041).getHeight() -px)
          self.getControl(100).setHeight(self.getControl(100).getHeight() -px)
          self.getControl(1001).setHeight(self.getControl(1001).getHeight() -px)
          self.getControl(10042).setHeight(self.getControl(10042).getHeight() -px)
          self.getControl(10043).setHeight(self.getControl(10043).getHeight() -px)
          self.getControl(10044).setPosition(self.getControl(10044).getX(),self.getControl(10044).getY() - px)
          self.getControl(1005).setVisible(False)
          self.getControl(100).setPosition(self.getControl(100).getX(),self.getControl(100).getY() + (px/2))

        self.getControl(1003).setLabel(self.title)

        for option in self.options:
            list_item = xbmcgui.ListItem(option , iconImage="", thumbnailImage="")
            self.getControl(10042).addItem(list_item)
        self.setFocusId(10042)
        self.getControl(10042).setEnabled(True)
    def onAction(self, action):
      pass
      
    def onClick( self, control_id ):
      logger.info(control_id)
      if control_id == 10042:
        self.result = self.getControl(10042).getSelectedPosition()
        self.close()
      if control_id == 1002:  
        self.close()

        
        
        
class MainWindow(xbmcgui.WindowXML):
    def __init__(self, xml_name, fallback_path):
        self.history=[]
        global WindowXML
        WindowXML = self
            
    def Start(self):
        self.timeload = 0
        self.item = Item(channel="channelselector", action="mainlist")
        self.itemlist = navigation.NextItem(self.item)
        self.doModal()

    def onInit(self):
        self.getControl(500).setVisible(False)
        self.AddItems()
        
    def AddItems(self):
        self.getControl(301).setVisible(False)
        self.getControl(302).setVisible(False)
        self.getControl(303).setVisible(False)
        
        if (self.item.channel=="channelselector" and self.item.action=="mainlist") or (self.item.channel=="novedades" and self.item.action=="mainlist") or (self.item.channel=="buscador" and self.item.action=="mainlist") or (self.item.channel=="channelselector" and self.item.action=="channeltypes"):
          WindowMode = 0
        elif self.item.channel=="channelselector" and self.item.action=="listchannels":
          WindowMode = 1
        else:
          WindowMode = 2
        
        control = 301 +  WindowMode
        self.control_list = self.getControl(control)
        self.control_list.setVisible(True)
        self.control_list.reset()

        if type(self.itemlist)==list: 
          if not self.itemlist[0].action=="go_back":
            if not (self.item.channel=="channelselector" and self.item.action=="mainlist"):
              self.itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail="%sthumb_atras.png"))
            else:
              self.itemlist.insert(0,Item(title="Salir", action="go_back",thumbnail="%sthumb_atras.png"))

        for x in range(len(self.itemlist)):
            nitem, title, thumbnail = navigation.ItemInfo(self.item, self.itemlist[x], WindowMode)
            
            list_item = xbmcgui.ListItem(title , iconImage=thumbnail, thumbnailImage=thumbnail)
            info_labels = {"Title": title, "FileName": title, "Plot": self.itemlist[x].plot}
            list_item.setInfo( "video", info_labels )
            if self.itemlist[x].fanart!="": list_item.setProperty('fanart_image', self.itemlist[x].fanart)
            self.control_list.addItem(list_item)
        
        self.control_list.setEnabled(True)
        self.setFocusId(control)
        self.getControl(400).setVisible(False)

    def LoadItem(self, item):
      self.getControl(301).setEnabled(False)
      self.getControl(302).setEnabled(False)
      self.getControl(303).setEnabled(False)
      self.getControl(400).setVisible(True)
      logger.info("-----------------------------------------------------------------------")
      logger.info("Item Recibido: " + item.tostring())
      logger.info("-----------------------------------------------------------------------")
      import time
      Start =  time.time()
      try:
        itemlist = navigation.NextItem(item)
      except Exception as e:
        import traceback
        logger.error(traceback.format_exc())
        from core import scrapertools
        from core import guitools
        patron = 'File "'+os.path.join(config.get_runtime_path(),"pelisalacarta","channels","").replace("\\","\\\\")+'([^.]+)\.py"'
        canal = scrapertools.find_single_match(traceback.format_exc(),patron)
        if canal:
          guitools.Dialog_OK(
            "Se ha producido un error en el canal " + canal,
            "Esto puede ser devido a varias razones: \n - El servidor no está disponible, o no esta respondiendo.\n - Cambios en el diseño de la web.\n - Etc...\nComprueba el log para ver mas detalles del error.")
        else:
          guitools.Dialog_OK(
            "Se ha producido un error en pelisalacarta",
            "Comprueba el log para ver mas detalles del error." )
        itemlist = None
      if type(itemlist)==list: 
        if not item == self.item: 
          self.history.append({"Item": self.item, "Position": self.control_list.getSelectedPosition(), "Itemlist": self.itemlist, "Time": self.timeload})
          
        self.timeload = time.time() - Start
        self.itemlist = itemlist
        self.item = item
        self.AddItems()
        self.UpdateInfo()
      else:
        self.getControl(400).setVisible(False)
        self.control_list.setEnabled(True)
        self.UpdateInfo()

    def onAction(self, action):
        self.UpdateInfo()

        if action == ACTION_PARENT_DIR or action==ACTION_PREVIOUS_MENU or action==ACTION_PREVIOUS_MENU2:
            self.Back()
        if action == ACTION_SELECT_ITEM:
            pass
        if action == ACTION_CONTEXT_MENU or action == ACTION_CONTEXT_MENU2:
           self.OpenMenu()
           
    def Back(self):
          self.getControl(400).setVisible(True)
          if len(self.history) ==0: self.close()
          else:
            self.item = self.history[len(self.history)-1]["Item"]
            position = self.history[len(self.history)-1]["Position"]
            self.timeload =  self.history[len(self.history)-1]["Time"]
            if self.history[len(self.history)-1]["Time"] > 4:
              self.itemlist = self.history[len(self.history)-1]["Itemlist"]
            else:
              self.itemlist = navigation.NextItem(self.item)   
            self.history = self.history[:-1]

            self.AddItems()
            self.control_list.selectItem(position)
            self.UpdateInfo()
          
    def onClick( self, control_id ):
        item = self.itemlist[self.control_list.getSelectedPosition()]
        if item.action == "go_back": 
          self.Back()
        else:
          self.LoadItem(item)

        
    def OpenMenu(self):
        item = self.itemlist[self.control_list.getSelectedPosition()]
        if item.context:
          Options = []
          RawOptions = item.context.split("|")
          for Option in RawOptions:
            Options.append(Option.split(",")[0])
          op = SelectWindow("ListDialog.xml",config.get_runtime_path()).setOptions("Menu", Options)
            
          if op >= 0:  
            import copy
            contextitem = copy.deepcopy(item)
            contextitem.refered_action = contextitem.action
            contextitem.action = RawOptions[op].split(",")[1]
            self.LoadItem(contextitem)

      
    def UpdateInfo(self):
      try:
        item = self.itemlist[self.control_list.getSelectedPosition()]
      except:
        self.getControl(201).setImage("") 
        self.getControl(202).setText("") 
        self.getControl(203).setText("")
        self.getControl(204).setVisible(True)
        self.getControl(205).setVisible(True)
        return
      
      if self.control_list.getId() == 303:
        if not item.action =="go_back" and not item.action == "search":
          if item.thumbnail!="" and not "thumb_error" in item.thumbnail and not "thumb_folder" in item.thumbnail and not "thumb_nofolder" in item.thumbnail: 
            if "%s" in item.thumbnail: thumbnail = item.thumbnail %(config.get_thumbnail_path(""))
            else: thumbnail = item.thumbnail
            self.getControl(201).setImage(thumbnail) 
            self.getControl(202).setText(item.title) 
            self.getControl(203).setText(item.plot)
            self.getControl(204).setVisible(False)
            self.getControl(205).setVisible(False)
          else:
            self.getControl(201).setImage("") 
            self.getControl(202).setText("") 
            self.getControl(203).setText("")
            self.getControl(204).setVisible(True)
            self.getControl(205).setVisible(True)
        else:
          self.getControl(201).setImage("") 
          self.getControl(202).setText("") 
          self.getControl(203).setText("")
          self.getControl(204).setVisible(True)
          self.getControl(205).setVisible(True)
      else:
        self.getControl(201).setImage("") 
        self.getControl(202).setText("") 
        self.getControl(203).setText("")
        self.getControl(204).setVisible(True)
        self.getControl(205).setVisible(True)

