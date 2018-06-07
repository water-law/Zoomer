# 环境：QGIS 3.0 + Qt5 + Pycharm

# 设置： Pycharm IDE -> File -> settings -> Project Interpreter -> add Local -> System Interpreter 添加 python 环境

C:\Program Files\QGIS 3.0\bin\python3.exe。

# 模板：从 http://www.dimitrisk.gr/qgis/creator/ 这个网站下载 PyQGIS 插件模板， 虽然是 PyQt4 的， 但改造成 PyQt5

不是问题，具体参考项目中的相关文件。

# 编译 ui 文件和 qrc  文件为 python 文件， 网上的教程大多是 PyQt4 的， 我这里是一个 trans.bat 脚本，写的不是很好，

看来要补下 bat 文件怎么写。。。

# 插件安装：找到 QGIS 的插件目录， 找不到的话有个方法， 先在 QGIS 安装一个 plugin builder 3 的插件， 然后全盘搜

pluginbuilder3(没有空格！！！), 举个例子， 我 QGIS 安装目录为： C:\Program Files\QGIS 3.0， 但是插件目录却在这里

C:\Users\zjp\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins， 可以看到该目录下有一个名为 pluginbuilder3

的目录， 这个就是 pluginbuilder3 插件， 将我们的 Zoomer 文件夹拷贝到 pluginbuilder3 同一级的目录即可。

