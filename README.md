# 环境：

QGIS 3.0 + Qt5 + Pycharm

# 设置：

 Pycharm IDE -> File -> settings -> Project Interpreter -> add Local -> System Interpreter 添加 python 环境

C:\Program Files\QGIS 3.0\bin\python3.exe。

# 模板：

从 http://www.dimitrisk.gr/qgis/creator/ 这个网站下载 PyQGIS 插件模板， 虽然是 PyQt4 的， 但改造成 PyQt5

不是问题，具体参考项目中的相关文件(注意：python 模块使用相对路径导入的尽量使用相对路径， 否则 QGIS 会报错)。

# 编译 ui 文件和 qrc  文件为 python 文件

 网上的教程大多是 PyQt4 的， 我这里是一个 static.bat 脚本，写的不是很好，看来要补下 bat 文件怎么写。。。

# 插件安装：

找到 QGIS 的插件目录， 找不到的话有个方法， 先在 QGIS 安装一个 plugin builder 3 的插件， 然后全盘搜 pluginbuilder3(没有空格！！！),

举个例子， 我 QGIS 安装目录为： C:\Program Files\QGIS 3.0， 但是插件目录却在这里

C:\Users\zjp\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins， 可以看到该目录下有一个名为 pluginbuilder3

的目录，这个就是 pluginbuilder3 插件， 将我们的 Zoomer 文件夹拷贝到 pluginbuilder3 同一级的目录即可。

# 单独使用 python 虚拟环境

使用 python3 内置库 python3 -m venv <dir_name>

 Pycharm IDE -> File -> settings -> Project Interpreter -> add Local -> System Interpreter 添加 python 环境

### 附加 c++ 版本的插件

解压 plugin_code_examples.zip 压缩包，用 vs2017 打开