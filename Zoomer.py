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
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction, QLabel
from qgis.core import *
# Initialize Qt resources from file resources.py
# Import the code for the dialog
from .model.tools import *


class Zoomer(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon("icon.png"), "Menu Item", self.iface.mainWindow())
        # connect the action to the run method
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
        uri.setConnection("localhost", "5432", "place", "postgres", "postgres")
        uri.setDataSource("public", "objnam", "geom")
        vlayer = self.iface.addVectorLayer(uri.uri(False), "layer name you like", "postgres")
        fields = vlayer.fields()
        fieldNames = fields.names()
        languages = all_languages()
        for i, fieldName in enumerate(fieldNames, 0):
            # 设置 field 别名
            vlayer.setFieldAlias(i, attribute_display('objnam', fieldName))
            if fieldName == 'fid':
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
            elif fieldName == 'objl':
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Enumeration", {}))
                # 设置默认值
                vlayer.setDefaultValueDefinition(i, QgsDefaultValue('1', True))
            elif fieldName == 'scamax':
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
                vlayer.setDefaultValueDefinition(i, QgsDefaultValue('25000000', True))
            elif fieldName == 'scamin':
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
                vlayer.setDefaultValueDefinition(i, QgsDefaultValue('1', True))
            elif fieldName == 'en_us':
                vlayer.setFieldAlias(i, languages['en-US'])
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
                vlayer.setDefaultValueDefinition(i, QgsDefaultValue("11", True))
            elif fieldName == 'zh_chs':
                vlayer.setFieldAlias(i, languages['zh-CHS'])
                vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
                # vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Hidden", {}))
                # vlayer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
                vlayer.setDefaultValueDefinition(i, QgsDefaultValue('None', True))
        formConfig = vlayer.editFormConfig()
        formConfig.setReadOnly(1, False)
        formConfig.setUiForm('./attributeform/Attribute_Form.ui')
        # 设置 python 脚本使用方式
        formConfig.setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
        formConfig.setInitFilePath(os.path.join(os.path.dirname(__file__), 'attributeform/attribute_form.py'))
        # 设置脚本入口函数
        formConfig.setInitFunction("formOpen")
        vlayer.setEditFormConfig(formConfig)
