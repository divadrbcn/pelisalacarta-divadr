# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parámetros de configuración (kodi)
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
import sys
import os
import xbmcaddon
import xbmc
PLATFORM_NAME = "kodi-isengard"
PLUGIN_NAME = "pelisalacarta"
__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString

def open_settings():
    __settings__.openSettings()

def get_setting(name):
    return __settings__.getSetting( name )

def set_setting(name,value):
    __settings__.setSetting( name,value )

def get_localized_string(code):
    dev = __language__(code)
    try:
        dev = dev.encode("utf-8")
    except:
        pass
    return dev


def get_runtime_path():
    return xbmc.translatePath( __settings__.getAddonInfo('Path') )

def get_data_path():
    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    
    # Parche para XBMC4XBOX
    if not os.path.exists(dev):
        os.makedirs(dev)
    
    return dev

# Test if all the required directories are created
def verify_directories_created():

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