import sip
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import *
from qgis.gui import QgsAttributeForm
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
        gbox = QGridLayout()
        gbox.setObjectName("grid")
        row = 1
        fields = myLayer.fields()
        for field in fields:
            fieldName = field.name()
            displayName = field.displayName()
            attrs = myFeature.attributes()
            if len(attrs) == 0:
                myLayer.deleteFeature(myFeature.id())
                # id 为 0 的 feature: 原因待排查
                break
            # FIXME: 对于 defaultValue 还需再进行仔细的检测
            defaultValue = myFeature.attribute(fieldName)
            label = QLabel(displayName)
            label.setObjectName("label_" + fieldName)
            tp = field.typeName()
            gbox.addWidget(label, row, 0)
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
            gbox.addWidget(f, row, 1)
            if fieldName in list(lang_obj.keys()):
                multi_lingual.append(fieldName)
                deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'delete.png')), "", self)
                deleteButton.setObjectName('delete_button_' + fieldName)
                deleteButton.clicked.connect(self.deleteField)
                gbox.addWidget(deleteButton, row, 2)
            else:
                pass
                # spacer = QSpacerItem(5, 15, QSizePolicy.Fixed, QSizePolicy.Fixed)
                # gbox.addItem(spacer, row, 2)
            row += 1

        hbox = QHBoxLayout()
        hbox.addStretch()

        okbutton = QPushButton('OK', self)
        cancelbutton = QPushButton('Cancel', self)
        okbutton.clicked.connect(self.validate)
        cancelbutton.clicked.connect(myForm.close)
        hbox.addWidget(okbutton)
        hbox.addWidget(cancelbutton)

        addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'plus.png')), "", self)
        addButton.setObjectName('add_button_' + fieldName)
        addButton.clicked.connect(self.tipDialog)
        gbox2 = QGridLayout()
        # FIXME: 布局有待确定
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)
        gbox2.addWidget(addButton, 1, 3)
        gbox2.addItem(spacer2)

        vbox.addLayout(gbox)
        vbox.addLayout(gbox2)
        vbox.addLayout(hbox)

    def validate(self):
        QMessageBox.information(self, "", "AA")

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
        deleteButton = self.findChild(QPushButton, "delete_button_"+fieldName)
        try:
            layout.removeWidget(label)
            layout.removeWidget(box)
            layout.removeWidget(deleteButton)
            sip.delete(label)
            sip.delete(box)
            sip.delete(deleteButton)
        except:
            QMessageBox.critical(self, "ERROR", "can not delete none type widget!")


def formOpen(dialog, layer, feature):
    # TODO: 移除 dialog 默认布局
    global myForm
    global myLayer
    global myFeature
    myForm = dialog.parent()
    # QgsAttributeForm
    mode = dialog.mode()
    QMessageBox.information(dialog, "dialog", str(mode))
    if myForm is not None:
        # 非属性表单模式, 属性表单模式的dialog.parent() 没有 layout
        # TODO: 区分 QgsAttributeForm 的各种模式
        childs = myForm.findChildren(QWidget)
        # QMessageBox.information(None, myForm.objectName(), str(type(myForm)))
        ly = myForm.layout()
        # QMessageBox.information(None, ly.objectName(), str(type(ly)))
        myLayer = layer
        myFeature = feature
        attrs = feature.attributes()
        # for x in childs:
        #     QMessageBox.information(None, x.objectName(), str(type(x)))
        # for x in attrs:
        # dialog is an instance of class qgis.gui.QgsAttributeForm
        # handler=MyEventHandler(dialog);
        # dialog.button.connect(handle.OnAddLanguage, cliced)
        myDialog = dialog.findChild(QDialog, "Dialog")
        buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
        # buttonBox.accepted.connect(validate)
        # buttonBox.rejected.connect(dialog.close)
        layout = dialog.layout()
        myWidget = MyWidget(myDialog)
        layout.addWidget(myWidget)
    else:
        QMessageBox.information(None, "myForm is None", "NNN")


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
        pgbox = parent.findChild(QGridLayout, "grid")
        row = pgbox.rowCount() + 1
        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        for k, v in lang_obj.items():
            if v['name'] == text:
                fieldName = k
                break
        label = QLabel(lang_obj[fieldName]['name'], parent)
        label.setObjectName("label_" + fieldName)
        f = QLineEdit(parent)
        f.setText("NULL")
        f.setObjectName(fieldName)
        deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'delete.png')), "", parent)
        deleteButton.setObjectName('delete_button_'+fieldName)
        deleteButton.clicked.connect(parent.deleteField)
        pgbox.addWidget(label, row, 0)
        pgbox.addWidget(f, row, 1)
        pgbox.addWidget(deleteButton, row, 2)
        if fieldName not in multi_lingual:
            multi_lingual.append(fieldName)
        self.close()

