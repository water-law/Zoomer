from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from model.tools import *

obj = obj_dict()
lang_obj = obj['languages']
field_fid = None
field_objl = None
field_scamax = None
field_scamin = None
field_zh_chs = None
field_en_us = None

myForm = None
myLayer = None
gridLayout = None
myDialog = None
newFieldDialog = None

label_fid = None
label_objl = None
label_scamax = None
label_scamin = None
label_zh_chs = None
label_en_us = None

multi_lingual = ["zh_chs", "en_us"]


class AddFieldDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add a New Country Language Support')
        self.initUI()

    def initUI(self):
        # QPushButton(const QIcon & icon, const QString & text, QWidget * parent = Q_NULLPTR)
        okbutton = QPushButton('OK')
        cancelbutton = QPushButton('Cancel')
        okbutton.clicked.connect(self.addField)
        cancelbutton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(okbutton)
        hbox.addWidget(cancelbutton)

        langLabel = QLabel('choose language')
        langbutton = QComboBox()
        langbutton.setObjectName("lang")
        language_list = list(lang_obj.keys())
        target_list = []
        for lang in language_list:
            if globals().get("field_" + lang, None) is None:
                target_list.append(lang)
        langbutton.addItems(target_list)

        gbox = QGridLayout()
        gbox.addWidget(langLabel, 1, 0)
        gbox.addWidget(langbutton, 1, 1)

        vbox = QVBoxLayout()
        vbox.setObjectName("base")
        vbox.addStretch()
        vbox.addLayout(gbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def unload(self):
        newFieldDialog = None
        self.close()

    def addField(self):
        current_rows = gridLayout.rowCount()
        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        label = QLabel()
        label.setText(text)
        gridLayout.addWidget(label, current_rows + 1, 0)
        lineEdit = QLineEdit()
        gridLayout.addWidget(lineEdit, current_rows + 1, 1)
        addButton = QPushButton(QIcon("E:/projects/Zoomer/plus.png"), "", self)
        gridLayout.addWidget(addButton, current_rows + 1, 2)
        deleteButton = QPushButton(QIcon("E:/projects/Zoomer/delete.png"), "", self)
        gridLayout.addWidget(deleteButton, current_rows + 1, 3)
        newFieldDialog = None
        self.close()


def setLayerProperties(dialog, layer, feature):
    """
    设置 field 是否可编辑只需在 ui 文件中关联控件的可编辑属性
    在 Label 中指定标签名字
    """
    fields = layer.fields()
    for field in fields:
        fieldName = field.name()
        displayName = field.displayName()
        field_obj = obj.get(fieldName, None)
        if field_obj is not None:
            child = dialog.findChild(QLabel, "label_" + fieldName)
            child.setText(displayName)
        elif fieldName in list(lang_obj.keys()):
            child = dialog.findChild(QLabel, "label_" + fieldName)
            child.setText(displayName)


def formOpen(dialog, layer, feature):
    # dialog is an instance of class qgis.gui.QgsAttributeForm
    global myForm
    global myLayer
    myForm = dialog
    myLayer = layer
    type_mapping = {"Integer": QSpinBox, "Enumeration": QComboBox, "TextEdit": QLineEdit, "Default": QLineEdit}
    global okButton
    global resetButton
    global gridLayout
    global myDialog
    myDialog = dialog.findChild(QDialog, "Dialog")
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
            component_type = obj.get(field).get('type')
            componentType = type_mapping.get(component_type, type_mapping['Default'])
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
        addButton.clicked.connect(addFieldDialog)
        if globals().get("delete_button_"+lingual) is None:
            globals()["delete_button_"+lingual] = deleteButton
        # ls = dir(gridLayout)
        # for i in ls:
        #     QMessageBox.information(None, "ADD Field", i)
        # deleteButton.clicked.connect("rer")

    setLayerProperties(dialog, layer, feature)
    buttonBox.accepted.connect(validate)
    buttonBox.rejected.connect(myForm.close)
    resetButton.clicked.connect(myForm.resetValues)


def addFieldDialog():
    global newFieldDialog
    newFieldDialog = AddFieldDialog()
    newFieldDialog.show()


def deleteField(s):
    # gridLayout.removeWidget(deleteButton)
    QMessageBox.information(None, "Delete Field", s)


def validate():
    # Make sure that the name field isn't empty.
    for key in globals().keys():
        if key.startswith("field_"):
            if key[6:] in multi_lingual:
                QMessageBox.information(None, key, key[6:])
    # if not len(globals()['field_fid'].text()) > 0:
    #     msgBox = QMessageBox()
    #     msgBox.setText("fid field can not be null.{}")
    #     msgBox.exec_()
    # elif not int(globals()['field_scamin'].text()) > 0:
    #     msgBox = QMessageBox()
    #     msgBox.setText("scamin field can not be null.")
    #     msgBox.exec_()
    # else:
    #     pass

