from qgis.PyQt.QtWidgets import *
from qgis.core import QgsEditorWidgetSetup
from model.tools import *

obj = obj_dict()
lang_obj = obj['languages']
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
    for fieldName in fieldNames:
        # 设置 field 别名
        field_obj = obj.get(fieldName, None)
        if field_obj is not None:
            child = dialog.findChild(QLabel, "label_" + fieldName)
            child.setText(field_obj.get('display', None))
        elif fieldName in list(lang_obj.keys()):
            child = dialog.findChild(QLabel, "label_" + fieldName)
            child.setText(lang_obj[fieldName].get('name', None))


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
    # okButton = dialog.findChild(QPushButton, "okButton")
    # resetButton = dialog.findChild(QPushButton, "resetButton")
    buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    resetButton = buttonBox.button(QDialogButtonBox.Reset)
    # if fidLabel is None:
    for lingual in multi_lingual:
        label = dialog.findChild(QLabel, "label_{}".format(lingual))
        addButton = dialog.findChild(QPushButton, "add_button_{}".format(lingual))
        deleteButton = dialog.findChild(QPushButton, "delete_button_{}".format(lingual))
        if globals()[lingual+"Label"] is None:
            globals()[lingual+"Label"] = label
        if globals().get("add_button_"+lingual) is None:
            globals().setdefault("add_button_"+lingual, addButton)
        addButton.clicked.connect(addField)
        if globals().get("delete_button_"+lingual) is None:
            globals().setdefault("delete_button_"+lingual, deleteButton)

    setLayerProperties(dialog, layer, feature)
    buttonBox.accepted.connect(validate)
    buttonBox.rejected.connect(myDialog.close)
    # okButton.clicked.connect(validate)
    resetButton.clicked.connect(myDialog.resetValues)


def test():
    QMessageBox.information(None, "AA", "AsASAS")


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

