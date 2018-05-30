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
from PyQt5 import QtCore, QtWidgets
from Ui_Zoomer import Ui_Zoomer
# create the dialog for Zoomer
class ZoomerDialog(QtWidgets.QDialog):
  def __init__(self):
    QtWidgets.QDialog.__init__(self)
    # Set up the user interface from Designer. 
    self.ui = Ui_Zoomer()
    self.ui.setupUi(self)