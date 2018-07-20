"""
/***************************************************************************
Name			 	 : Zoom plugin
Description          : Zooms to a point when the user hits the button.
Date                 : 29/May/18 
copyright            : (C) 2018 by Dimitris Kavroudakis
email                : onoma@in.gr 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction
from qgis.core import *
# Initialize Qt resources from file resources.py
# noinspection PyUnresolvedReferences
from .resources import *
# Import the code for the dialog
from .ZoomerDialog import ZoomerDialog

class Zoomer: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/Zoomer/icon.png"), \
        "Menu Item", self.iface.mainWindow())
    # connect the action to the run method
    # QObject.connect(self.action, pyqtSignal("activated()"), self.run)
    self.action.triggered.connect(self.run)

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Menu Item", self.action)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&Menu Item",self.action)
    self.iface.removeToolBarIcon(self.action)
    # Remove the qrc file in memory.
    qCleanupResources()

  # run method that performs all the real work
  def run(self): 
    # create and show the dialog 
    dlg = ZoomerDialog() 
    # show the dialog
    dlg.show()
    result = dlg.exec_() 
    # See if OK was pressed
    if result == 1: 
      # do something useful (delete the line containing pass and
      # substitute with your code
      pass 
