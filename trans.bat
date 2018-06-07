@echo off
call "C:\Program Files\QGIS 3.0\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.0\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.0\bin\py3_env.bat"

@echo on
# pyrcc5 -o resources.py resources.qrc && pyuic5 -o Ui_Zoomer.py Ui_Zoomer.ui

FOR %%F IN (*.qrc) DO pyrcc5 -o %%F.py %%F && FOR %%F IN (*.ui) DO pyuic5 -o %%F.py %%F
