# 项目说明
本项目为开发 QGIS 地名标注插件。release 下有 python 插件基础模板， 需要者请自行下载。

# 安装方法
将整个 Zoomer 目录拷贝到 C:/Users/[用户名]/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/ 下，
如果不行的话看看用户目录下是否有 .qgis 的目录， 进入该目录应能找到插件安装目录。除此之外， 你可能需要根据
model/sql.md 的文件创建相应的 pgsql 数据库（使用 pgsql shell）。

# 开发环境
1. 系统环境变量配置
PYTHONHOME:
C:\Program Files\QGIS 3.0\apps\Python36
---------------------------------------------
PYTHONPATH:
C:\Program Files\QGIS 3.0\apps\Python36\Lib
C:\Program Files\QGIS 3.0\apps\qgis\python
C:\Program Files\QGIS 3.0\apps\Python36\Scripts
-----------------------------------------------
PATH:
C:\Program Files\QGIS 3.0\bin
C:\Program Files\QGIS 3.0\apps\qgis\bin
C:\Program Files\QGIS 3.0\apps\Python36\Scripts
C:\Qt\Qt5.10.0\5.10.0\msvc2015_64\bin
C:\Qt\Qt5.10.0\Tools\QtCreator\bin
2. IDE 配置
pycharm2017.3.8(使用社区版本即可)， File->Open-> 选择 Zoomer 文件夹，加载项目后，File->Settings->Project Interpreter
-> Add Local -> C:\Program Files\QGIS 3.0\bin\python3.exe。
Edit Configurations-> + -> Python -> Script Path 选择 Zoomer 文件夹下的 sync 文件。

# 项目文件简略说明

sync: 将 Zoomer 文件夹同步到插件目录下的 python 脚本
trans.bat: 将 Zoomer 目录下的资源文件转为 python 文件
