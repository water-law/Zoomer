import sip
import traceback
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import *
from qgis.gui import QgsAttributeForm
from model.tools import *
_translate = QCoreApplication.translate

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
        gbox.setObjectName("grid_attribute_form")
        row = 1
        fields = myLayer.fields()
        for field in fields:
            fieldName = field.name()
            displayName = field.displayName()
            attributes = myFeature.attributes()
            # FIXME: id 为 0 的 feature: 原因待排查
            if len(attributes) == 0:
                myLayer.deleteFeature(myFeature.id())
                break
            # FIXME: 对于 defaultValue 还需再进行仔细的检测
            # FIXME: 默认值是否应配置到字典中， 字典中还应包含控件类型和自定义控件类型和数据库类型及其默认值
            # FIXME: 字典中可能还需包括数据库类型信息表明是 PostGIS 还是 SQLite
            defaultValue = myFeature.attribute(fieldName)
            typeName = field.typeName()
            # QMessageBox.information(self, fieldName, str(type(defaultValue)))
            if typeName == 'int4':
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                f = QSpinBox()
                if fieldName == 'fid':
                    f.setEnabled(False)
                try:
                    f.setValue(defaultValue)
                except TypeError:
                    f.setValue(0)
                f.setObjectName(fieldName)
                gbox.addWidget(f, row, 1)
            elif typeName == 'objl_type':
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                f = QComboBox()
                enums = list()
                for enum in obj['objl']['enums']:
                    enums.append(enum['description'])
                f.addItems(enums)
                if defaultValue in enums:
                    f.setCurrentText(defaultValue)
                f.setObjectName(fieldName)
                gbox.addWidget(f, row, 1)
            elif fieldName in ['zh_chs', 'en_us']:
                # 默认显示中英文
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                f = QLineEdit()
                # 中英文可能被置为""或者NULL
                try:
                    f.setText(defaultValue)
                except TypeError:
                    f.setText("NULL")
                f.setObjectName(fieldName)
                gbox.addWidget(f, row, 1)
                multi_lingual.append(fieldName)
                deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/delete.png')), "", self)
                deleteButton.setObjectName('delete_button_' + fieldName)
                deleteButton.clicked.connect(self.deleteField)
                gbox.addWidget(deleteButton, row, 2)
            elif fieldName in list(lang_obj.keys()):
                # 数据库中还未有此列
                if defaultValue is None:
                    continue
                elif defaultValue == "":  # "" 屏蔽某个语言
                    continue
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                f = QLineEdit()
                try:
                    f.setText(defaultValue)
                except TypeError:
                    # 该列值在数据库为 NULL
                    f.setText("NULL")
                f.setObjectName(fieldName)
                gbox.addWidget(f, row, 1)
                multi_lingual.append(fieldName)
                deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/delete.png')), "", self)
                deleteButton.setObjectName('delete_button_' + fieldName)
                deleteButton.clicked.connect(self.deleteField)
                gbox.addWidget(deleteButton, row, 2)
            else:
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                f = QLineEdit()
                f.setText("NULL")
                f.setObjectName(fieldName)
                gbox.addWidget(f, row, 1)
            row += 1

        hbox = QHBoxLayout()
        hbox.addStretch()

        okButton = QPushButton('OK', self)
        cancelButton = QPushButton('Cancel', self)
        okButton.clicked.connect(self.validate)
        cancelButton.clicked.connect(myForm.close)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/plus.png')), "", self)
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
        d = AddLanguageDialog(self)
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
        except TypeError:
            # delete None 会引起 TypeError
            QMessageBox.critical(self, "TypeError", traceback.format_exc())
        except RuntimeError:
            # 重复删除会引起 RuntimeError
            QMessageBox.critical(self, "RuntimeError", traceback.format_exc())


def formOpen(dialog, layer, feature):
    # TODO: 移除 dialog 默认布局
    global myForm
    global myLayer
    global myFeature
    myForm = dialog.parent()
    # QgsAttributeForm.AddFeatureMode
    mode = dialog.mode()
    if myForm is not None:
        # QMessageBox.information(dialog, "dialog", str(mode))
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
        # dialog.button.connect(handle.OnAddLanguage, cliced)
        myDialog = dialog.findChild(QDialog, "Dialog")
        buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
        layout = dialog.layout()
        myWidget = MyWidget(myDialog)
        layout.addWidget(myWidget)
    else:
        QMessageBox.information(dialog, "dialog", dialog.objectName())
        QMessageBox.information(None, "myForm is None", "NNN")


class AddLanguageDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Add a New Country Language Support')
        self.initUI()

    def initUI(self):
        self.setWindowTitle(_translate('attr_form', 'Title'))
        # QPushButton(const QIcon & icon, const QString & text, QWidget * parent = Q_NULLPTR)
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        okButton.clicked.connect(self.addField)
        cancelButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

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
        gbox = parent.findChild(QGridLayout, "grid_attribute_form")
        row = gbox.rowCount() + 1
        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        for k, v in lang_obj.items():
            if v['name'] == text:
                fieldName = k
                break
        label = QLabel(lang_obj[fieldName]['name'], parent)
        label.setObjectName("label_" + fieldName)
        f = QLineEdit(parent)
        defaultValue = myFeature.attribute(fieldName)
        try:
            f.setText(defaultValue)
        except TypeError:
            f.setText("NULL")
        f.setObjectName(fieldName)
        deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/delete.png')), "", parent)
        deleteButton.setObjectName('delete_button_'+fieldName)
        deleteButton.clicked.connect(parent.deleteField)
        gbox.addWidget(label, row, 0)
        gbox.addWidget(f, row, 1)
        gbox.addWidget(deleteButton, row, 2)
        if fieldName not in multi_lingual:
            multi_lingual.append(fieldName)
        self.close()

