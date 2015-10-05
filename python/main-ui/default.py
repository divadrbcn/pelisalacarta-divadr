# -*- coding: utf-8 -*-
import ui
from core import logger
from core.item import Item
from core import config
import xbmc

logger.info("pelisalacarta 4 ui begin")
config.verify_directories_created()
# Open main window
ui.MainWindow("MainWindow.xml",config.get_runtime_path()).Start()
