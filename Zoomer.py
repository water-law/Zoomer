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
from .model.tools import attribute_display, all_languages


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
        uri = QgsDataSourceUri()
        uri.setConnection("localhost", "5432", "demo", "postgres", "postgres")
        uri.setDataSource("public", "objnam", "geom")
        vlayer = self.iface.addVectorLayer(uri.uri(False), "layer name you like", "postgres")

        formConfig = vlayer.editFormConfig()
        attrs = vlayer.attributeList()
        fields = vlayer.fields()
        languages = all_languages()
        for index in attrs:
            field_name = fields[index].name()
            # 设置 field 别名
            vlayer.setFieldAlias(index, attribute_display('objnam', field_name))
            if field_name == 'fid':
                # 设置某个 field 是否可写
                formConfig.setReadOnly(index, False)
            elif field_name == 'objl':
                # 设置默认值
                vlayer.setDefaultValueDefinition(index, QgsDefaultValue('1', False))
            elif field_name == 'scamax':
                vlayer.setDefaultValueDefinition(index, QgsDefaultValue('25000000', False))
            elif field_name == 'scamin':
                vlayer.setDefaultValueDefinition(index, QgsDefaultValue('1', False))
            elif field_name == 'level':
                vlayer.setDefaultValueDefinition(index, QgsDefaultValue('1', False))
            elif field_name.replace('_', '-') in languages:
                fields.remove(index)
        # vectorLayer->setEditorWidgetSetup(1, QgsEditorWidgetSetup("Enumeration", QVariantMap()));
        vlayer.setEditFormConfig(formConfig)


