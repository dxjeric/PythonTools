## 执行

1. copyFile执行模式说明：

    * 1: 拷贝当前修改的文件和新增的配置文件，地图文件

    * 2: 拷贝全部配置以及所有地图文件

    * 3: 根据输入的提交ID拷贝当前提交的配置文件以及地图文件

2. 执行方式: copyFile.exe modid
3. **特别说明** 每次执行都会删除远端的文件，然后再拷贝。所以每次拷贝前请先将远端文件拷贝至内网

## python相关

1. python 3.x版本

2. 安装 pywin32 
    
* pip install pywin32
    
3.  安装 Pyinstaller

    * pip install PyInstaller
    * [pyinstaller官网](http://www.pyinstaller.org/)

4. 生成exe

    cmd执行 pyinstaller copyFile.py
    
    记得拷贝config.ini配置文件

## 代码

1. copyFile.py **python源码**

2. config.ini  **配置文件 说明如下 **

    |        配置项        |               参数值                | 说明                                                         |    section     |
    | :------------------: | :---------------------------------: | :----------------------------------------------------------- | :------------: |
    |    globalUserName    |            true or false            | 1. 是否使用全局名称 如果和内网不一致 尝试修改这个字段为false 根据对应下方对应方式处理<br/>2. 如果为true    获取的是git config --global user.name 设置方式 git config --global user.name 花名<br/>3. 如果为false   获取的是git config --local user.name 设置方式 git config --local user.name 花名 |    [COMMON]    |
    |      projectDir      |          C:\work\NyClient\          | git所在工作目录 可以是相对路径                               |    [COMMON]    |
    |   configCheckPath    |           Config/Server/            | 配置文件相对路径(相对projectDir)                             |  [CONFIGFILE]  |
    | remoteConfigRootPath | \\192.168.10.154\诺亚手游内\config  | 远程拷贝的根目录 增加对应的(globalUserName)文件夹            |  [CONFIGFILE]  |
    |   mapJsonCheckPath   |           Config/MapData/           | 地图json文件位置                                             |  [CONFIGMAP]   |
    | mapNavmeshCheckPath  |            ExportedObj/             | 地图navmesh文件位置                                          |  [CONFIGMAP]   |
    |  mapNavmeshFileType  |                 bin                 | navmesh文件扩展名                                            |  [CONFIGMAP]   |
    |  remoteMapRootPath   | \\192.168.10.154\诺亚手游内\mapData | 地图数据远程根目录 增加对应的(globalUserName)文件夹          |  [CONFIGMAP]   |
|  serverBatFileName   |      copyConfigFromClient.bat       | 内网拷贝的批处理文件                                         | [CONFIGSERVER] |
    