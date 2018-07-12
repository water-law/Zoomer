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
 This script initializes the plugin, making it known to QGIS.
"""
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtWidgets import QApplication, QMessageBox


def name():
    return "Zoom plugin"


def description():
    return "Zooms to a point when the user hits the button."


def version():
    return "Version 0.1"


def qgisMinimumVersion():
    return "1.0"


def classFactory(iface):
    # load Zoomer class from file Zoomer
    from .Zoomer import Zoomer
    translator = QTranslator()
    translator.load("zh_CN")
    app = QApplication.instance()
    app.installTranslator(translator)
    return Zoomer(iface)
