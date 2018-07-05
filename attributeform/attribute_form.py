from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from qgis.gui import QgsAttributeForm
from model.tools import *

obj = obj_dict()
print(obj)
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


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setObjectName("base")
        vbox.addStretch()
        label_fid = QLabel()
        label_fid.setText("objl")
        label_fid.setObjectName("label_" + "objl")
        field_fid = QComboBox()
        field_fid.addItems(["A", "B", "C"])
        field_fid.setObjectName("objl")
        hbox = QHBoxLayout()
        # hbox.addStretch()
        hbox.addWidget(label_fid)
        hbox.addWidget(field_fid)
        # vbox.addLayout(hbox)
        self.setLayout(hbox)

    def addField(self, text):
        pass

    def deleteField(self, text):
        pass


def formOpen(dialog, layer, feature):
    import sip
    # dialog is an instance of class qgis.gui.QgsAttributeForm
    # handler=MyEventHandler(dialog);
    # dialog.button.connect(handle.OnAddLanguage, cliced)
    myDialog = dialog.findChild(QDialog, "Dialog")
    childs = dialog.findChildren(QWidget)
    layout = dialog.layout()
    # for x in childs:
    #     layout.removeWidget(x)
    #     sip.delete(x)
    myWidget = MyWidget(dialog)
    layout.addWidget(myWidget)
    # my.show()


def addFieldDialog():
    global newFieldDialog
    if newFieldDialog is not None:
         newFieldDialog = None
    newFieldDialog = AddFieldDialog()
    newFieldDialog.show()


def validate():
    # Make sure that the name field isn't empty.
    for key in globals().keys():
        if key.startswith("field_"):
            if key[6:] in multi_lingual:
                QMessageBox.information(None, key, key[6:])


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
                target_list.append(lang_obj[lang]['name'])
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

    def addField(self):
        global gridLayout
        global myForm
        current_rows = gridLayout.rowCount()
        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        for k, v in lang_obj.items():
            if v['name'] == text:
                fieldName = k
                break
        label = QLabel(myForm)
        label.setText(text)
        label.setObjectName('label_'+fieldName)
        gridLayout.addWidget(label, current_rows + 1, 0)
        lineEdit = QLineEdit(myForm)
        lineEdit.setObjectName(fieldName)
        gridLayout.addWidget(lineEdit, current_rows + 1, 1)
        addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'plus.png')), "", myForm)
        addButton.setObjectName("add_button_"+fieldName)
        gridLayout.addWidget(addButton, current_rows + 1, 2)
        deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'delete.png')), "", myForm)
        deleteButton.setObjectName('delete_button_'+fieldName)
        if globals().get("label_" + fieldName) is None:
            globals()["label_" + fieldName] = label
        if globals().get("add_button_"+fieldName) is None:
            globals()["add_button_"+fieldName] = addButton
        addButton.clicked.connect(addFieldDialog)
        if globals().get("delete_button_"+fieldName) is None:
            globals()["delete_button_"+fieldName] = deleteButton
        gridLayout.addWidget(deleteButton, current_rows + 1, 3)
        newFieldDialog = None
        self.close()

