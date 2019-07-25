#! python3
# encoding: utf8
## python 版本3.x
## 支持配置 config.ini
import os, io, shutil, errno, sys
import configparser
from git import Git
from enum import Enum

# 基础配置
projectDir = r"../"
Project = False
globalUserName = False

# 配置拷贝
remoteConfigRootPath = r"\\192.168.10.154\诺亚手游内\config"
configCheckPath = r"Config/Server/"
configCheckPathLen = len(configCheckPath)

# 地图拷贝
mapJsonCheckPath 		= r"Config/MapData/"
mapJsonCheckPathLen		= len(mapJsonCheckPath)
mapNavmeshCheckPath 	= r"ExportedObj/"
mapNavmeshCheckPathLen 	= len(mapNavmeshCheckPath)
mapNavmeshFileType  	= 'bin'
remoteMapRootPath		= r"\\192.168.10.154\诺亚手游内\mapData"

# 服务器批处理
serverBatFileName = "copyConfigFromClient.bat"

# 用户远端拷贝地址
userRemoteConfigPath	= ""
userRemoteMapPath		= ""

# 文件类型枚举
class CopyType(Enum):
	invalid		= -1
	config 		= 1
	mapJson 	= 2
	mapNavmesh 	= 3

# 加载配置项
def initGlobalInfo():
	global remoteConfigRootPath
	global configCheckPath
	global configCheckPathLen
	global projectDir
	global project
	global globalUserName
	global mapJsonCheckPath
	global mapJsonCheckPathLen
	global mapNavmeshCheckPath
	global mapNavmeshCheckPathLen
	global mapNavmeshFileType
	global remoteMapRootPath
	
	config = configparser.ConfigParser()
	if config.read('config.ini', 'utf8') and config['COMMON']:
		if config['COMMON']['projectDir']:
			projectDir = config['COMMON']['projectDir']

		if config['COMMON']['globalUserName']:
			globalUserName = (config['COMMON']['globalUserName'].lower() == 'true')

		if config['CONFIGFILE']['remoteConfigRootPath']:
			remoteConfigRootPath = config['CONFIGFILE']['remoteConfigRootPath']

		if config['CONFIGFILE']['configCheckPath']:
			configCheckPath = config['CONFIGFILE']['configCheckPath']

		if config['CONFIGMAP']['mapJsonCheckPath']:
			mapJsonCheckPath = config['CONFIGMAP']['mapJsonCheckPath']
		
		if config['CONFIGMAP']['mapNavmeshCheckPath']:
			mapNavmeshCheckPath = config['CONFIGMAP']['mapNavmeshCheckPath']

		if config['CONFIGMAP']['mapNavmeshFileType']:
			mapNavmeshFileType = "."+config['CONFIGMAP']['mapNavmeshFileType']

		if config['CONFIGMAP']['remoteMapRootPath']:
			remoteMapRootPath = config['CONFIGMAP']['remoteMapRootPath']

		if config['CONFIGSERVER']['serverBatFileName']:
			serverBatFileName = config['CONFIGSERVER']['serverBatFileName']


	if not os.path.exists(remoteConfigRootPath):
		print(remoteConfigRootPath, "is invalid dir")
		return False

	if projectDir[-1:] == '/' or projectDir[-1:] == '\\':
		projectDir = projectDir[0:-1]

	if configCheckPath[-1:] != '/' and configCheckPath[-1:] != '\\':
		configCheckPath = configCheckPath + "/"

	if mapJsonCheckPath[-1:] != '/' and mapJsonCheckPath[-1:] != '\\':
		mapJsonCheckPath = mapJsonCheckPath + "/"
	
	if mapNavmeshCheckPath[-1:] != '/' and mapNavmeshCheckPath[-1:] != '\\':
		mapNavmeshCheckPath = mapNavmeshCheckPath + "/"

	configCheckPathLen 		= len(configCheckPath)
	mapJsonCheckPathLen 	= len(mapJsonCheckPath)
	mapNavmeshCheckPathLen 	= len(mapNavmeshCheckPath)

	if os.path.exists(projectDir+"/.git"):
		project = Git(projectDir)
	else:
		print(projectDir, "is invalid git repo")
		return False

	return True

# 获取用户名称
def getUserName():
	global project
	global globalUserName
	if globalUserName:
		return project.config("--global", "user.name")
	else:
		return project.config("--local", "user.name")

# 创建目录
def createNewRemoteRootDir(rootDir):
	if os.path.isdir(rootDir):
		shutil.rmtree(rootDir)

# 生成远端根目录
def genRemoteDir(bMkdir):
	global userRemoteConfigPath
	global userRemoteMapPath
	# 根据用户名创建新的远程文件夹
	userName = getUserName()
	userRemoteConfigPath = str.format(r"{}/{}", remoteConfigRootPath, userName)
	userRemoteMapPath 	 = str.format(r"{}/{}", remoteMapRootPath, userName)
	if bMkdir:
		createNewRemoteRootDir(userRemoteConfigPath)
		createNewRemoteRootDir(userRemoteMapPath)

	print("拷贝用户: ", userName, "<<<")

def checkNeedCopy(filePath):
	global configCheckPath
	global configCheckPathLen
	global mapJsonCheckPath
	global mapJsonCheckPathLen
	global mapNavmeshCheckPath
	global mapNavmeshCheckPathLen
	global mapNavmeshFileType

	if len(filePath) > 0:
		findex = filePath.find(configCheckPath)
		if findex > -1:
			return CopyType.config, filePath[findex+configCheckPathLen:]
		
		findex = filePath.find(mapJsonCheckPath)
		if findex > -1:
			return CopyType.mapJson, filePath[findex+mapJsonCheckPathLen:]

		findex = filePath.find(mapNavmeshCheckPath)
		if findex > -1 and os.path.splitext(filePath)[-1] == mapNavmeshFileType:
			return CopyType.mapNavmesh, filePath[findex+mapNavmeshCheckPathLen:]

	return CopyType.invalid, ""

# 拷贝单个文件
def copyOneFile(filePath, remotePath):
	print(str.format("拷贝 {}", filePath))
	remoteDir = os.path.dirname(remotePath)
	try:		
		os.makedirs(remoteDir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			print("copyOneFile create dir erorr!", os.strerror(e.errno))
			return False
	shutil.copy(filePath, remotePath)

	return True


# 根据文件列表拷贝到对应目录
def copyFileByList(fl):
	global userRemoteConfigPath
	global userRemoteMapPath
	needCopyFileCount	 = 0
	totalCopyFileCount	= 0
	for filePath in fl:
		filePath = str.format("{}/{}", projectDir, filePath)
		_copyType, relativePath = checkNeedCopy(filePath)
		remoteFilePath = ""
		if _copyType == CopyType.config:
			needCopyFileCount = needCopyFileCount + 1
			remoteFilePath = str.format(r"{}/{}", userRemoteConfigPath, relativePath)
		elif _copyType == CopyType.mapJson:
			needCopyFileCount = needCopyFileCount + 1
			remoteFilePath = str.format(r"{}/mapEditData/{}", userRemoteMapPath, relativePath)
		elif _copyType == CopyType.mapNavmesh:
			needCopyFileCount = needCopyFileCount + 1
			remoteFilePath = str.format(r"{}/navmeshFile/{}", userRemoteMapPath, relativePath)

		if remoteFilePath != "" and copyOneFile(filePath, remoteFilePath):
			totalCopyFileCount = totalCopyFileCount + 1
			
	
	if totalCopyFileCount != needCopyFileCount:
		print("-------------------------------------------------------------------")
		print("----------------------拷贝文件异常！！！！！-----------------------")
		print("-------------------------------------------------------------------")
		return False
	else:
		print("-------------------------------------------------------------------")
		print("----------------------------拷贝成功-------------------------------")
		print("-------------------------------------------------------------------")
		return True

# 获取修改的文件列表 新增文件列表
def getModifyFiles():
	global project
	# 修改和待添加的文件
	allFiles = project.ls_files("-o", "--exclude-standard") + '\n' + project.ls_files("-m")
	# 返回文件列表
	return allFiles.splitlines()

# 拷贝对应的修改文件 未commit的文件
def processModify():
	# 开始拷贝文件夹
	fl = getModifyFiles()
	return copyFileByList(fl)


# 拷贝全文件
def processCopyAll():
	global userRemoteConfigPath
	global userRemoteMapPath
	
	# 全拷贝配置
	configDir = str.format("{}/{}", projectDir, configCheckPath)
	shutil.copytree(configDir, userRemoteConfigPath)

	# 全拷贝地图
	mapJsonDir = str.format("{}/{}", projectDir, mapJsonCheckPath)
	remoteJsonDir = str.format("{}/mapEditData", userRemoteMapPath)
	shutil.copytree(mapJsonDir, remoteJsonDir)
	mapNavmeshDir = str.format("{}/{}", projectDir, mapNavmeshCheckPath)
	remoteNavmeshDir = str.format("{}/navmeshFile", userRemoteMapPath)
	shutil.copytree(mapNavmeshDir, remoteNavmeshDir)
	print("-------------------------------------------------------------------")
	print("----------------------------拷贝成功-------------------------------")
	print("-------------------------------------------------------------------")

# 根据提交SHA-1找出修改文件
def getCommitFileBySHA(sha):
	try:
		fi = project.show(sha, "--name-only", "--pretty=format:")
		return fi.splitlines()
	except Exception as e:
		return False


# 根据提交文件内容拷贝
def processCommit():
	sha = input("请输入提交ID\n提交ID在git log中查看93cc057eb2 或者工具showlog中 SHA-1)\n")
	fl = False
	while not fl:
		fl = getCommitFileBySHA(sha)
		if not fl:
			sha = input("请输入正确的提交ID\n")

	return copyFileByList(fl)

# 从远端拷贝到内网
def copyRemoteConfigToServer():
	global userRemoteConfigPath
	global userRemoteMapPath
	global serverBatFileName

	serverBatFilePath = str.format("../../{}", serverBatFileName)
	if not os.path.isfile(serverBatFilePath):
		print("-------------------------------------------------------------------")
		print("-------------------------批处理不存在------------------------------")
		print("-------------------------------------------------------------------")
		return
	
	cmd = str.format("cd ../../ & call {} {} {}", serverBatFileName, userRemoteConfigPath, userRemoteMapPath)
	os.system(cmd)

def main():
	global userRemoteConfigPath
	global userRemoteMapPath

	try:
		print("初始化 ... ")
		if not initGlobalInfo():
			return

		# 生成远端地址
		if len(sys.argv) > 0 and sys.argv[1] != '4':
			genRemoteDir(True)
		else:
			genRemoteDir(False)

		if userRemoteConfigPath == "" or userRemoteMapPath == "" :
			print("-------------------------------------------------------------------")
			print("-------------------------远端地址异常------------------------------")
			print("-------------------------------------------------------------------")
			return
		
		if len(sys.argv) == 1 or sys.argv[1] == '1':
			print("开始拷贝修改配置 >>> ")
			processModify()
		elif sys.argv[1] == '2':
			print("开始拷贝全部配置 >>> ")
			processCopyAll()
		elif sys.argv[1] == '3':
			print("开始拷贝提交配置 >>> ")
			processCommit()
		elif sys.argv[1] == '4':
			print("开始拷贝配置 >>> ")
			copyRemoteConfigToServer()
		else:
			print("-------------------------------------------------------------------")
			print("-----------------------启动参数异常！ 找程序------------------------")
			print("-------------------------------------------------------------------")
	except (KeyboardInterrupt,EOFError):
		pass
	except Exception as e:
		print(type(e), e)
		print("-------------------------------------------------------------------")
		print("--------------------------执行异常！ 找程序------------------------")
		print("-------------------------------------------------------------------")
	finally:
		os.system("pause")

main()
