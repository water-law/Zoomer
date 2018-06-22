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
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import *
# Initialize Qt resources from file resources.py
# Import the code for the dialog
from .ZoomerDialog import ZoomerDialog


class Zoomer:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon("icon.png"), "Menu Item", self.iface.mainWindow())
        # connect the action to the run method
        # QObject.connect(self.action, pyqtSignal("activated()"), self.run)
        self.action.setObjectName("test Action")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Menu Item", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Menu Item", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # create and show the dialog
        project = QgsProject.instance()
        project.read("C:/Users/zjp/QGIS/pg.qgs")
        uri = QgsDataSourceUri()
        # set host name, port, database name, username and password
        uri.setConnection("localhost", "5432", "demo", "postgres", "postgres")
        # set database schema, table name, geometry column and optionally
        # subset (WHERE clause)
        uri.setDataSource("public", "objnam", "the_geom")
        vlayer = QgsVectorLayer(uri.uri(False), "layer name you like", "postgres")
        if not vlayer.isValid():
            dlg = ZoomerDialog()
            # show the dialog
            dlg.show()
            result = dlg.exec_()
            # See if OK was pressed
            if result == 1:
                # do something useful (delete the line containing pass and
                # substitute with your code
                pass
        # for field in vlayer.fields():
        #     QMessageBox.information(None, field.name(), field.typeName())
        features = vlayer.getFeatures()
        # for feature in features:
        #     geom = feature.geometry()
        #     QMessageBox.information(None, "Feature ID", str(feature.id()))
        #     if geom.wkbType() == QgsWkbTypes.Point:
        #         x = geom.asPoint()
        #         QMessageBox.information(None, "Point", x.asWkt())
        #     attrs = feature.attributes()
        #     QMessageBox.information(None, "attrs", str(attrs))
        vlayer.selectAll()
        project.addMapLayer(vlayer)


