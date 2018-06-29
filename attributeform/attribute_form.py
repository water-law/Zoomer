from qgis.PyQt.QtWidgets import *
from qgis.core import QgsEditorWidgetSetup
from model.tools import *

fidField = None
objlField = None
scamaxField = None
scaminField = None
levelField = None
zh_chsField = None
en_usField = None
myDialog = None
fidLabel = None
objlLabel = None
scamaxLabel = None
scaminLabel = None
levelLabel = None
zh_chsLabel = None
en_usLabel = None

addPushButton = None


def setLayerProperties(dialog, layer, feature):
    """
    设置 field 是否可编辑只需在 ui 文件中关联控件的可编辑属性
    在 Label 中指定标签名字
    """
    fields = layer.fields()
    fieldNames = fields.names()
    languages = all_languages()
    for i, fieldName in enumerate(fieldNames, 0):
        # 设置 field 别名
        layer.setFieldAlias(i, attribute_display('objnam', fieldName))
        child = dialog.findChild(QLabel, fieldName + "_2")
        child.setText(attribute_display('objnam', fieldName))


def addField(layer):
    QMessageBox.information(None, "XXX", "ASAs")
    # try:
    #     layer.setEditorWidgetSetup(7, QgsEditorWidgetSetup("TextEdit", {}))
    # except:
    #     QMessageBox.information(None, "XXX", "ASAs")


def formOpen(dialog, layer, feature):
    # dialog is an instance of class qgis.gui.QgsAttributeForm
    global myDialog
    myDialog = dialog
    global fidField
    global objlField
    global scamaxField
    global scaminField
    global levelField
    global zh_chsField
    global en_usField
    global fidLabel
    global objlLabel
    global scamaxLabel
    global scaminLabel
    global levelLabel
    global zh_chsLabel
    global en_usLabel
    global addPushButton
    fidField = dialog.findChild(QSpinBox, "fid")
    objlField = dialog.findChild(QComboBox, "objl")
    scamaxField = dialog.findChild(QSpinBox, "scamax")
    scaminField = dialog.findChild(QSpinBox, "scamin")
    levelField = dialog.findChild(QComboBox, "level")
    zh_chsField = dialog.findChild(QLineEdit, "zh_chs")
    en_usField = dialog.findChild(QLineEdit, "en_us")
    fidLabel = dialog.findChild(QLabel, "fid_2")
    objlLabel = dialog.findChild(QLabel, "pbjl_2")
    scamaxLabel = dialog.findChild(QLabel, "scamax_2")
    scaminLabel = dialog.findChild(QLabel, "scamin_2")
    levelLabel = dialog.findChild(QLabel, "level_2")
    addPushButton = dialog.findChild(QPushButton, "add")

    # if fidLabel is None:
    zh_chsLabel = dialog.findChild(QLabel, "zh_chs_2")
    en_usLabel = dialog.findChild(QLabel, "en_us_2")

    setLayerProperties(dialog, layer, feature)

    buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    resetButton = buttonBox.button(QDialogButtonBox.Reset)

    # Wire up our own signals.
    buttonBox.accepted.connect(validate)
    buttonBox.rejected.connect(myDialog.close)
    resetButton.clicked.connect(myDialog.resetValues)
    addPushButton.clicked.connect(addField(layer))


def validate():
    # Make sure that the name field isn't empty.
    if not len(fidField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("fid field can not be null.{}")
        msgBox.exec_()
    elif not int(scaminField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("scamin field can not be null.")
        msgBox.exec_()
    else:
        pass

