from qgis.PyQt.QtWidgets import *
from qgis.core import QgsEditorWidgetSetup
from model.tools import *

class_name = get_class_name()

fidField = None
objlField = None
scamaxField = None
scaminField = None
zh_chsField = None
en_usField = None

myDialog = None
myLayer = None

fidLabel = None
objlLabel = None
scamaxLabel = None
scaminLabel = None
zh_chsLabel = None
en_usLabel = None

multi_lingual = ["zh_chs", "en_us"]


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
        if i >= 4:
            continue
        layer.setFieldAlias(i, attribute_display(class_name, fieldName))
        child = dialog.findChild(QLabel, "label_" + fieldName)
        child.setText(attribute_display(class_name, fieldName))


def formOpen(dialog, layer, feature):
    # dialog is an instance of class qgis.gui.QgsAttributeForm
    global myDialog
    global myLayer
    myDialog = dialog
    myLayer = layer
    global fidField
    global objlField
    global scamaxField
    global scaminField
    global fidLabel
    global objlLabel
    global scamaxLabel
    global scaminLabel
    global okButton
    global resetButton
    fidField = dialog.findChild(QSpinBox, "fid")
    objlField = dialog.findChild(QComboBox, "objl")
    scamaxField = dialog.findChild(QSpinBox, "scamax")
    scaminField = dialog.findChild(QSpinBox, "scamin")
    fidLabel = dialog.findChild(QLabel, "label_fid")
    objlLabel = dialog.findChild(QLabel, "label_pbjl")
    scamaxLabel = dialog.findChild(QLabel, "label_scamax")
    scaminLabel = dialog.findChild(QLabel, "label_scamin")
    okButton = dialog.findChild(QPushButton, "okButton")
    resetButton = dialog.findChild(QPushButton, "resetButton")
    x = dialog.findChildren(QDialogButtonBox, "buttonBox")
    if x is not None:
        QMessageBox.information(None, "", "xxxxxx")
    # if fidLabel is None:
    for lingual in multi_lingual:
        label = dialog.findChild(QLabel, "label_{}".format(lingual))
        addButton = dialog.findChild(QPushButton, "add_button_{}".format(lingual))
        deleteButton = dialog.findChild(QPushButton, "delete_button_{}".format(lingual))
        if globals()[lingual+"Label"] is None:
            globals()[lingual+"Label"] = label
        if globals().get("add_button_"+lingual) is None:
            globals().setdefault("add_button_"+lingual, addButton)
            # addButton.clicked.connect()
        if globals().get("delete_button_"+lingual) is None:
            globals().setdefault("delete_button_"+lingual, deleteButton)

    setLayerProperties(dialog, layer, feature)
    okButton.clicked.connect(validate)
    resetButton.clicked.connect(myDialog.resetValues)


def addField():
    QMessageBox.information(None, "myLayer", str(type(myLayer)))
    try:
        myLayer.setEditorWidgetSetup(7, QgsEditorWidgetSetup("TextEdit", {}))
    except:
        QMessageBox.information(None, "XXX", "ASAs")


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

