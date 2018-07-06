import sip
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import *
from model.tools import *

obj = obj_dict()
print(obj)
lang_obj = obj['languages']
print(lang_obj)

multi_lingual = list()


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setObjectName("base")
        vbox.addStretch()
        self.setLayout(vbox)
        vbox = self.layout()
        fields = myLayer.fields()
        for field in fields:
            fieldName = field.name()
            displayName = field.displayName()
            attrs = myFeature.attributes()
            if len(attrs) == 0:
                myLayer.deleteFeature(myFeature.id())
                # id 为 0 的 feature: 原因待排查
                break
            defaultValue = myFeature.attribute(fieldName)
            label = QLabel(displayName)
            label.setObjectName("label_" + fieldName)
            tp = field.typeName()
            hbox = QHBoxLayout()
            hbox.addStretch()
            hbox.addWidget(label)
            if tp == 'int4':
                f = QSpinBox()
                if fieldName == 'fid':
                    f.setEnabled(False)
                try:
                    f.setValue(defaultValue)
                except:
                    f.setValue(0)
            elif tp == 'objl_type':
                f = QComboBox()
                enums = list()
                for x in obj['objl']['enums']:
                    enums.append(x['description'])
                f.addItems(enums)
                if defaultValue in enums:
                    f.setCurrentText(defaultValue)
            else:
                f = QLineEdit()
                f.setText("NULL")
            f.setObjectName(fieldName)

            hbox.addWidget(f)
            if fieldName in list(lang_obj.keys()):
                multi_lingual.append(fieldName)
                addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'plus.png')), "", self)
                deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'delete.png')), "", self)
                addButton.setObjectName('add_button_'+fieldName)
                deleteButton.setObjectName('delete_button_' + fieldName)
                addButton.clicked.connect(self.tipDialog)
                deleteButton.clicked.connect(self.deleteField)
                hbox.addWidget(addButton)
                hbox.addWidget(deleteButton)
            vbox.addLayout(hbox)

    def tipDialog(self):
        d = AddFieldDialog(self)
        d.show()

    def deleteField(self):
        senderName = self.sender().objectName()
        fieldName = '_'.join(senderName.rsplit("_")[2:])
        multi_lingual.remove(fieldName)
        layout = self.layout()
        label = self.findChild(QLabel, "label_"+fieldName)
        box = self.findChild(QLineEdit, fieldName)
        addButton = self.findChild(QPushButton, "delete_button_"+fieldName)
        deleteButton = self.findChild(QPushButton, "add_button_"+fieldName)
        try:
            layout.removeWidget(label)
            layout.removeWidget(box)
            layout.removeWidget(addButton)
            layout.removeWidget(deleteButton)
            sip.delete(label)
            sip.delete(box)
            sip.delete(addButton)
            sip.delete(deleteButton)
        except:
            QMessageBox.critical(self, "ERROR", "can not delete none type widget!")


def formOpen(dialog, layer, feature):
    global myLayer
    global myFeature
    myLayer = layer
    myFeature = feature
    attrs = feature.attributes()
    # for x in attrs:
    # dialog is an instance of class qgis.gui.QgsAttributeForm
    # handler=MyEventHandler(dialog);
    # dialog.button.connect(handle.OnAddLanguage, cliced)
    myDialog = dialog.findChild(QDialog, "Dialog")
    layout = dialog.layout()
    myWidget = MyWidget(myDialog)
    layout.addWidget(myWidget)


def validate():
    # Make sure that the name field isn't empty.
    QMessageBox.information(None, "validate", "there is something to be do.")


class AddFieldDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
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
            if lang not in multi_lingual:
                target_list.append(lang_obj[lang]['name'])
        langbutton.addItems(target_list)

        gbox = QGridLayout()
        gbox.addWidget(langLabel, 1, 0)
        gbox.addWidget(langbutton, 1, 1)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(gbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def addField(self):
        parent = self.parent()
        vbox = parent.findChild(QVBoxLayout, "base")

        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        for k, v in lang_obj.items():
            if v['name'] == text:
                fieldName = k
                break
        label = QLabel(lang_obj[fieldName]['name'], parent)
        label.setObjectName("label_" + fieldName)
        hbox = QHBoxLayout(parent)
        hbox.addStretch()
        hbox.addWidget(label)
        f = QLineEdit(parent)
        f.setText("NULL")
        f.setObjectName(fieldName)
        hbox.addWidget(f)
        addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'plus.png')), "", parent)
        addButton.setObjectName("add_button_"+fieldName)
        addButton.clicked.connect(parent.tipDialog)
        deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'delete.png')), "", parent)
        deleteButton.setObjectName('delete_button_'+fieldName)
        deleteButton.clicked.connect(parent.deleteField)
        hbox.addWidget(addButton)
        hbox.addWidget(deleteButton)
        vbox.addLayout(hbox)
        if fieldName not in multi_lingual:
            multi_lingual.append(fieldName)
        self.close()

