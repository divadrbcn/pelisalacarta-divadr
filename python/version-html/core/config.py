# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Gestión de parámetros de configuración - Server
#-------------------------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#-------------------------------------------------------------------------------
# Creado por: 
# Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------------------
import os,re
from core.item import Item
import logger
PLATFORM_NAME="mediaserver"

settings_dic ={}
    
def open_settings():
    Opciones =[]
    from xml.dom import minidom
    settings=""
    while len(settings)<> os.path.getsize(menufilepath) or len(settings)==0:
      settings = open(menufilepath, 'rb').read()
    xmldoc= minidom.parseString(settings)
    for category in xmldoc.getElementsByTagName("category"):
      for setting in category.getElementsByTagName("setting"):
        if setting.getAttribute("type") =="sep":
          Opciones.append(["" ,"" , setting.getAttribute("type") ,"" ,"" ,"","","",category.getAttribute("label")])
        else:
          Opciones.append([setting.getAttribute("label") ,setting.getAttribute("id") , setting.getAttribute("type") ,setting.getAttribute("lvalues") ,setting.getAttribute("values") ,get_setting(setting.getAttribute("id")),setting.getAttribute("option"),setting.getAttribute("enabled"),category.getAttribute("label")])
    from platformcode import cliente
    cliente.Acciones().AbrirConfig(Opciones)

 
def get_setting(name):
    global settings_dic
    if name in settings_dic:
      return settings_dic[name]
    else:
      return ""

    
def load_settings():
    global settings_dic
    defaults = {}
    from xml.etree import ElementTree
    settings=""
    encontrado = False
    #Lee el archivo XML (si existe)
    if os.path.exists(configfilepath):
      while len(settings)<> os.path.getsize(configfilepath) or len(settings)==0:
        settings = open(configfilepath, 'rb').read()
      root = ElementTree.fromstring(settings)
      for target in root.findall("setting"):
        settings_dic[target.get("id")] = target.get("value")

          

    defaultsettings=""
    while len(defaultsettings)<> os.path.getsize(menufilepath) or len(defaultsettings)==0:
      defaultsettings = open(menufilepath, 'rb').read()
    root = ElementTree.fromstring(defaultsettings)
    for category in root.findall("category"):
      for target in category.findall("setting"):
        if target.get("id"):
          defaults[target.get("id")] = target.get("default")
      
    for key in defaults:
      if not key in settings_dic:
        settings_dic[key] =  defaults[key]
    set_settings(settings_dic)


def set_setting(name,value):
    settings_dic[name]=value
    from xml.dom import minidom
    #Crea un Nuevo XML vacio
    new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
    new_settings_root = new_settings.documentElement
    
    for key in settings_dic:
      nodo = new_settings.createElement("setting")
      nodo.setAttribute("value",settings_dic[key])
      nodo.setAttribute("id",key)    
      new_settings_root.appendChild(nodo)
      
    fichero = open(configfilepath, "w")
    fichero.write(new_settings.toprettyxml(encoding='utf-8'))
    fichero.close()

def set_settings(JsonRespuesta):
    for Ajuste in JsonRespuesta:
      settings_dic[Ajuste]=JsonRespuesta[Ajuste].encode("utf8")
    from xml.dom import minidom
    #Crea un Nuevo XML vacio
    new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
    new_settings_root = new_settings.documentElement
    
    for key in settings_dic:
      nodo = new_settings.createElement("setting")
      nodo.setAttribute("value",settings_dic[key])
      nodo.setAttribute("id",key)    
      new_settings_root.appendChild(nodo)
      
    fichero = open(configfilepath, "w")
    fichero.write(new_settings.toprettyxml(encoding='utf-8'))
    fichero.close()
    


def get_localized_string(code):
    translationsfile = open(TRANSLATION_FILE_PATH,"r")
    translations = translationsfile.read()
    translationsfile.close()
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code

def get_data_path():
    return os.path.join( os.path.expanduser("~") , ".pelisalacarta" )

def get_runtime_path():
    return os.getcwd()
# Test if all the required directories are created
def verify_directories_created():
    logger.info("Comprobando directorios")
    if not os.path.exists(get_data_path()): os.mkdir(get_data_path())
    
    config_paths = [["library_path",     "Library"],
                    ["downloadpath",     "Downloads"],
                    ["downloadlistpath", os.path.join("Downloads","List")],
                    ["bookmarkpath",     "Favorites"],
                    ["cache.dir",        "Cache"],
                    ["cookies.dir",      "Cookies"]]
                             
    for setting, default in config_paths:
      path = get_setting(setting)
      if path=="":
          path = os.path.join( get_data_path() , default)
          set_setting(setting , path)
          
      if not get_setting(setting).lower().startswith("smb") and not os.path.exists(get_setting(setting)):
        os.mkdir(get_setting(setting))
                    
            
def get_thumbnail_path(preferred_thumb=""):
    WEB_PATH = ""
    
    if preferred_thumb=="":
        thumbnail_type = get_setting("thumbnail_type")
        if thumbnail_type=="": thumbnail_type="2"
        
        if thumbnail_type=="0":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/squares/"
    else:
        WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/"+preferred_thumb+"/"
        
    return WEB_PATH
    
# Fichero de configuración
menufilepath= os.path.join(get_runtime_path(),"platformcode", "settings.xml")
configfilepath = os.path.join( get_data_path() , "settings.xml")
if not os.path.exists(get_data_path()): os.mkdir(get_data_path())   
# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
load_settings()