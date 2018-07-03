from qgis.PyQt.QtWidgets import *
from model.tools import *

obj = obj_dict()
lang_obj = obj['languages']
field_fid = None
field_objl = None
field_scamax = None
field_scamin = None
field_zh_chs = None
field_en_us = None

myDialog = None
myLayer = None
gridLayout = None

label_fid = None
label_objl = None
label_scamax = None
label_scamin = None
label_zh_chs = None
label_en_us = None

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
    type_mapping = {"Integer": QSpinBox, "Enumeration": QComboBox, "TextEdit": QLineEdit, "Default": QLineEdit}
    global okButton
    global resetButton
    global gridLayout
    gridLayout = dialog.findChild(QGridLayout, "gridLayout")
    obj_fields = list(obj.keys())
    for field in obj_fields:
        if field in ['display', 'code']:
            continue
        if field == 'languages':
            languages = obj.get('languages', None)
            if languages is None:
                continue
            for language in list(languages.keys()):
                globals()["field_" + language] = dialog.findChild(QLineEdit, language)
                if globals().get("label_" + field) is None:
                    globals()["label_" + field] = dialog.findChild(QLabel, "label_" + field)
        elif globals().get("field_" + field) is None:
            type = obj.get(field).get('type')
            componentType = type_mapping.get(type, type_mapping['Default'])
            globals()["field_" + field] = dialog.findChild(componentType, field)
            if globals().get("label_" + field) is None:
                globals()["label_" + field] = dialog.findChild(QLabel, "label_"+field)
    buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    resetButton = buttonBox.button(QDialogButtonBox.Reset)
    for lingual in multi_lingual:
        label = dialog.findChild(QLabel, "label_{}".format(lingual))
        addButton = dialog.findChild(QPushButton, "add_button_{}".format(lingual))
        deleteButton = dialog.findChild(QPushButton, "delete_button_{}".format(lingual))
        if globals().get("label_" + lingual) is None:
            globals()["label_" + lingual] = label
        if globals().get("add_button_"+lingual) is None:
            globals()["add_button_"+lingual] = addButton
        addButton.clicked.connect(addButton.hide)
        if globals().get("delete_button_"+lingual) is None:
            globals()["delete_button_"+lingual] = deleteButton
        deleteButton.clicked.connect(deleteField)

    setLayerProperties(dialog, layer, feature)
    buttonBox.accepted.connect(validate)
    buttonBox.rejected.connect(myDialog.close)
    resetButton.clicked.connect(myDialog.resetValues)


def addField():
    QMessageBox.information(None, "ADD Field", "sds")


def deleteField():
    gridLayout.remove(None)
    QMessageBox.information(None, "Delete Field", "asa")


def validate():
    # Make sure that the name field isn't empty.
    fid = globals()['field_fid']
    if fid is None:
        QMessageBox.information(None, "fid", "NONE")
    if not len(globals()['field_fid'].text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("fid field can not be null.{}")
        msgBox.exec_()
    elif not int(globals()['field_scamin'].text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("scamin field can not be null.")
        msgBox.exec_()
    else:
        pass

