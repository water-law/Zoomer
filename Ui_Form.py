from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox, QMessageBox

fidField = None
objlField = None
scamaxField = None
scaminField = None
levelField = None
zh_chsField = None
en_usField = None
myDialog = None


def formOpen(dialog, layer, feature):
    global myDialog
    myDialog = dialog
    global fidField
    global objlField
    global scamaxField
    global scaminField
    global levelField
    global zh_chsField
    global en_usField
    fidField = dialog.findChild(QLineEdit, "fid")
    objlField = dialog.findChild(QLineEdit, "objl")
    scamaxField = dialog.findChild(QLineEdit, "scamax")
    scaminField = dialog.findChild(QLineEdit, "scamin")
    levelField = dialog.findChild(QLineEdit, "level")
    zh_chsField = dialog.findChild(QLineEdit, "zh_chs")
    en_usField = dialog.findChild(QLineEdit, "en_us")
    buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    QMessageBox.information(myDialog, "From", str(type(myDialog)))
    # Disconnect the signal that QGIS has wired up for the dialog to the button box.
    # buttonBox.accepted.disconnect(myDialog.accept)

    # Wire up our own signals.
    buttonBox.accepted.connect(validate)
    # buttonBox.rejected.connect(myDialog.reject)


def validate():
    # Make sure that the name field isn't empty.
    # QMessageBox.information(None, "QQ", "QQQQQQQQQ")
    if not len(fidField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("fid field can not be null.{}")
        msgBox.exec_()
    elif not int(scaminField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("scamin field can not be null.")
        msgBox.exec_()
    else:
        # Return the form as accpeted to QGIS.
        myDialog.accept()
