from qgis.core import *
from qgis.PyQt.QtWidgets import *
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


def setLayerProperties(dialog, layer, feature):
    # 可在此设置图层 Label 字段的是否显示
    # 在 ui 文件中控制图层 field 字段的是否可编辑， 控件类型
    """
    设置 field 是否可编辑只需在 ui 文件中关联控件的可编辑属性
    设置 field 控件类型
    无需设置别名， 在 Label 中指定标签名字
    """
    global fidLabel
    global objlLabel
    global scamaxLabel
    global scaminLabel
    global levelLabel
    global zh_chsLabel
    global en_usLabel
    fields = layer.fields()
    fieldNames = fields.names()
    languages = all_languages()
    for i, fieldName in enumerate(fieldNames, 0):
        # 设置 field 别名
        layer.setFieldAlias(i, attribute_display('objnam', fieldName))
        child = dialog.findChild(QLabel, fieldName + "_2")
        child.setText(attribute_display('objnam', fieldName))
        if fieldName == 'id':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Hidden", {}))
        elif fieldName == 'fid':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
        elif fieldName == 'objl':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Enumeration", {}))
            # 设置默认值
            layer.setDefaultValueDefinition(i, QgsDefaultValue('1', True))
        elif fieldName == 'scamax':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
            layer.setDefaultValueDefinition(i, QgsDefaultValue('25000000', True))
        elif fieldName == 'scamin':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Range", {}))
            layer.setDefaultValueDefinition(i, QgsDefaultValue('1', True))
        elif fieldName == 'level':
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Enumeration", {}))
            # layer.setDefaultValueDefinition(i, QgsDefaultValue('1', False))
        elif fieldName == 'en_us':
            layer.setFieldAlias(i, languages['en-US'])
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
            layer.setDefaultValueDefinition(i, QgsDefaultValue("11", True))
        elif fieldName == 'zh_chs':
            layer.setFieldAlias(i, languages['zh-CHS'])
            layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("TextEdit", {}))
            # layer.setEditorWidgetSetup(i, QgsEditorWidgetSetup("Hidden", {}))
            layer.setDefaultValueDefinition(i, QgsDefaultValue('None', True))


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
    fidField = dialog.findChild(QLineEdit, "fid")
    objlField = dialog.findChild(QLineEdit, "objl")
    scamaxField = dialog.findChild(QLineEdit, "scamax")
    scaminField = dialog.findChild(QLineEdit, "scamin")
    levelField = dialog.findChild(QLineEdit, "level")
    zh_chsField = dialog.findChild(QLineEdit, "zh_chs")
    en_usField = dialog.findChild(QLineEdit, "en_us")
    fidLabel = dialog.findChild(QLabel, "fid_2")
    objlLabel = dialog.findChild(QLabel, "pbjl_2")
    scamaxLabel = dialog.findChild(QLabel, "scamax_2")
    scaminLabel = dialog.findChild(QLabel, "scamin_2")
    levelLabel = dialog.findChild(QLabel, "level_2")

    # if fidLabel is None:
    #     QMessageBox.information(dialog, "Label", str("no find."))
    zh_chsLabel = dialog.findChild(QLabel, "zh_chs_2")
    en_usLabel = dialog.findChild(QLabel, "en_us_2")

    setLayerProperties(dialog, layer, feature)

    buttonBox = dialog.findChild(QDialogButtonBox, "buttonBox")
    resetButton = buttonBox.button(QDialogButtonBox.Reset)

    # Wire up our own signals.
    buttonBox.accepted.connect(validate)
    buttonBox.rejected.connect(myDialog.close)
    resetButton.clicked.connect(myDialog.resetValues)


def validate():
    # Make sure that the name field isn't empty.
    if not len(fidField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("fid field can not be null.{}")
        msgBox.exec_()
        pass
    elif not int(scaminField.text()) > 0:
        msgBox = QMessageBox()
        msgBox.setText("scamin field can not be null.")
        msgBox.exec_()
        pass
    else:
        # Return the form as accpeted to QGIS.
        pass

