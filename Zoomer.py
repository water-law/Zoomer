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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtCore import QFileInfo
from qgis.core import *
# Initialize Qt resources from file resources.py
# Import the code for the dialog
# Use the resources.qrc file to set plugin's icon
from .resources import *
from .model.tools import *


class Zoomer:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.user_plugin_dir = QFileInfo(
            QgsApplication.qgisUserDatabaseFilePath()).path() + '/python/plugins'
        QMessageBox.information(None, "path", self.user_plugin_dir)
        self.plugin_builder_path = os.path.dirname(__file__)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/Zoomer/icon.png"),
            "Zoomer", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Zoomer", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Zoomer", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        import os
        QMessageBox.information(None, "dir", os.path.abspath(__file__))
        uri = QgsDataSourceUri()
        dbConfig = db_config()
        connection = tuple(dbConfig['connection'].values())
        datasource = tuple(dbConfig['datasource'].values())
        uri.setConnection(*connection)
        uri.setDataSource(*datasource)
        layer = self.iface.addVectorLayer(uri.uri(False), "layer name you like", "postgres")
        # return
        formConfig = layer.editFormConfig()
        fields = layer.fields()
        fieldNames = fields.names()
        obj = obj_dict()
        lang_obj = obj['languages']
        for fieldName in fieldNames:
            i = fields.indexFromName(fieldName)
            field_obj = obj.get(fieldName, None)
            if field_obj is not None:
                # 设置 field 别名
                layer.setFieldAlias(i, field_obj.get('display', None))
                field_type = field_obj.get('type')
                if field_type == 'Integer':
                    layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
                    if fieldName == 'fid':
                        formConfig.setReadOnly(i, True)
                        # 设置默认值仅对新建要素时有效
                        layer.setDefaultValueDefinition(i, QgsDefaultValue('-1', False))
                    else:
                        layer.setDefaultValueDefinition(i, QgsDefaultValue('0', True))
                elif field_type == 'Enumeration':
                    layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Enumeration", {}))
                else:
                    layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
            elif fieldName in list(lang_obj.keys()):
                layer.setFieldAlias(i, lang_obj[fieldName].get('name', None))
                layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
            else:
                layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))

        formConfig.setUiForm('./attributeform/Attribute_Form.ui')
        # 设置 python 脚本使用方式
        formConfig.setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
        formConfig.setInitFilePath(os.path.join(os.path.dirname(__file__), 'attributeform/attribute_form.py'))
        # 设置脚本入口函数
        formConfig.setInitFunction("formOpen")
        layer.setEditFormConfig(formConfig)
