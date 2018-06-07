# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Zoomer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Zoomer(object):
    def setupUi(self, Zoomer):
        Zoomer.setObjectName("Zoomer")
        Zoomer.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Zoomer)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Zoomer)
        self.buttonBox.accepted.connect(Zoomer.accept)
        self.buttonBox.rejected.connect(Zoomer.reject)
        QtCore.QMetaObject.connectSlotsByName(Zoomer)

    def retranslateUi(self, Zoomer):
        _translate = QtCore.QCoreApplication.translate
        Zoomer.setWindowTitle(_translate("Zoomer", "Zoomer"))

