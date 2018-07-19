@echo off
call "C:\Program Files\QGIS 3.0\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.0\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.0\bin\py3_env.bat"

@echo on
pylupdate5 attributeform/attribute_form.py -ts zh_CN.ts