import sip
import traceback
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import *
from qgis.gui import QgsAttributeForm
from model.tools import *
from qgs.utils import wrapString
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
                inputWidget = QSpinBox()
                if fieldName == 'fid':
                    inputWidget.setEnabled(False)
                try:
                    inputWidget.setValue(defaultValue)
                except TypeError:
                    inputWidget.setValue(0)
                inputWidget.setObjectName(fieldName)
                gbox.addWidget(inputWidget, row, 1)
            elif typeName == 'objl_type':
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                inputWidget = QComboBox()
                enums = list()
                for enum in obj['objl']['enums']:
                    enums.append(enum['description'])
                inputWidget.addItems(enums)
                if defaultValue in enums:
                    inputWidget.setCurrentText(defaultValue)
                inputWidget.setObjectName(fieldName)
                gbox.addWidget(inputWidget, row, 1)
            elif fieldName in ['zh_chs', 'en_us']:
                # 默认显示中英文
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                inputWidget = QLineEdit()
                # 中英文可能被置为""或者NULL
                try:
                    inputWidget.setText(defaultValue)
                except TypeError:
                    inputWidget.setText("NULL")
                inputWidget.setObjectName(fieldName)
                gbox.addWidget(inputWidget, row, 1)
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
                inputWidget = QLineEdit()
                try:
                    inputWidget.setText(defaultValue)
                except TypeError:
                    # 该列值在数据库为 NULL
                    inputWidget.setText("NULL")
                inputWidget.setObjectName(fieldName)
                gbox.addWidget(inputWidget, row, 1)
                multi_lingual.append(fieldName)
                deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/delete.png')), "", self)
                deleteButton.setObjectName('delete_button_' + fieldName)
                deleteButton.clicked.connect(self.deleteField)
                gbox.addWidget(deleteButton, row, 2)
            else:
                label = QLabel(displayName)
                label.setObjectName("label_" + fieldName)
                gbox.addWidget(label, row, 0)
                inputWidget = QLineEdit()
                inputWidget.setText("NULL")
                inputWidget.setObjectName(fieldName)
                gbox.addWidget(inputWidget, row, 1)
            row += 1

        hbox = QHBoxLayout()
        hbox.addStretch()

        okButton = QPushButton('OK', self)
        cancelButton = QPushButton('Cancel', self)
        okButton.clicked.connect(self.validate)
        cancelButton.clicked.connect(myForm.resetValues)
        cancelButton.clicked.connect(baseDialog.close)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        addButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/plus.png')), "", self)
        addButton.setObjectName('add_button_' + fieldName)
        addButton.clicked.connect(self.tipDialog)
        buttonGbox = QGridLayout()
        # FIXME: 布局有待确定
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttonGbox.addWidget(addButton, 1, 3)
        buttonGbox.addItem(spacer)

        vbox.addLayout(gbox)
        vbox.addLayout(buttonGbox)
        vbox.addLayout(hbox)

    def validate(self):
        fields = myLayer.fields()
        for field in fields:
            fieldName = field.name()
            typeName = field.typeName()
            if typeName == "int4":
                child = self.findChild(QSpinBox, fieldName)
                value = child.value()
                if value <= 0:
                    QMessageBox.information(self, "field validate error", wrapString("{} 不能小于 0".format(fieldName)))
            elif typeName == "objl_type":
                child = self.findChild(QComboBox, fieldName)
                value = child.itemText(child.currentIndex())
                # 可能需要判定该语言列是否在合法语言中
            else:
                child = self.findChild(QLineEdit, fieldName)
                value = child.text()
                QMessageBox.information(self, fieldName, value)

    def tipDialog(self):
        dialog = AddLanguageDialog(self)
        dialog.show()

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
    global baseDialog
    global myForm
    global myLayer
    global myFeature
    baseDialog = dialog.parent()
    QMessageBox.information(None, "parent is {}".format(baseDialog.objectName()), baseDialog.objectName())
    myForm = dialog
    myLayer = layer
    myFeature = feature
    # QgsAttributeForm.AddFeatureMode
    mode = dialog.mode()
    if baseDialog is not None:
        # 非属性表单模式, 属性表单模式的dialog.parent() 没有 layout
        # TODO: 区分 QgsAttributeForm 的各种模式
        childs = baseDialog.findChildren(QLayout)
        # ly = myForm.layout()
        # QMessageBox.information(None, ly.objectName(), str(type(ly)))
        # for child in childs:
        #     QMessageBox.information(dialog, child.objectName(), str(type(child)))
        myDialog = dialog.findChild(QDialog, "Dialog")
        layout = dialog.layout()
        # try:
        #     layout.removeWidget(buttonBox)
        #     sip.delete(buttonBox)
        # except RuntimeError:
        #     QMessageBox.information(dialog, "RuntimeError", traceback.format_exc())
        # except Exception:
        #     QMessageBox.information(dialog, "Unknown Exception", traceback.format_exc())
        dialog.disconnectButtonBox()
        dialog.hideButtonBox()
        myWidget = MyWidget(myDialog)
        layout.addWidget(myWidget)


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
        okButton.clicked.connect(self.addLanguageField)
        cancelButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        langLabel = QLabel('choose language')
        langbutton = QComboBox()
        langbutton.setObjectName("lang")
        languageList = list(lang_obj.keys())
        targetList = []
        for lang in languageList:
            if lang not in multi_lingual:
                targetList.append(lang_obj[lang]['name'])
        langbutton.addItems(targetList)

        gbox = QGridLayout()
        gbox.addWidget(langLabel, 1, 0)
        gbox.addWidget(langbutton, 1, 1)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(gbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def addLanguageField(self):
        parent = self.parent()
        gbox = parent.findChild(QGridLayout, "grid_attribute_form")
        row = gbox.rowCount() + 1
        langbutton = self.findChild(QComboBox, "lang")
        text = langbutton.itemText(langbutton.currentIndex())
        for k, v in lang_obj.items():
            if v['name'] == text:
                fieldName = k
                break
        try:
            fields = myLayer.fields()
            field = fields.field(fieldName)
            displayName = field.displayName()
        except KeyError:
            # 数据库中未有该语言列
            displayName = lang_obj[fieldName]['name']
        label = QLabel(displayName, parent)
        label.setObjectName("label_" + fieldName)
        inputWidget = QLineEdit(parent)
        try:
            defaultValue = myFeature.attribute(fieldName)
            inputWidget.setText(defaultValue)
        except (KeyError, TypeError):
            inputWidget.setText("NULL")
        inputWidget.setObjectName(fieldName)
        deleteButton = QPushButton(QIcon(os.path.join(os.getcwd(), 'image/delete.png')), "", parent)
        deleteButton.setObjectName('delete_button_'+fieldName)
        deleteButton.clicked.connect(parent.deleteField)
        gbox.addWidget(label, row, 0)
        gbox.addWidget(inputWidget, row, 1)
        gbox.addWidget(deleteButton, row, 2)
        if fieldName not in multi_lingual:
            multi_lingual.append(fieldName)
        self.close()

