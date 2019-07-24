#! python3
# encoding: utf8
## python 版本3.x
## 支持配置 config.ini
import os, io, shutil, errno
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
 
def getUserName():
	global project
	global globalUserName
	if globalUserName:
		return project.config("--global", "user.name")
	else:
		return project.config("--local", "user.name")

def getModifyFiles():
	global project
	# 修改和待添加的文件
	allFiles = project.ls_files("-o", "--exclude-standard") + '\n' + project.ls_files("-m")
	# 返回文件列表
	return allFiles.splitlines()

class CopyType(Enum):
	invalid		= -1
	config 		= 1
	mapJson 	= 2
	mapNavmesh 	= 3



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

def createNewRemoteRootDir(rootDir):
	if os.path.isdir(rootDir):
		shutil.rmtree(rootDir)

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

def process():
	global project
	# 根据用户名创建新的远程文件夹
	userName = getUserName()
	userRemoteConfigPath = str.format(r"{}/{}", remoteConfigRootPath, userName)
	createNewRemoteRootDir(userRemoteConfigPath)
	userRemoteMapPath = str.format(r"{}/{}", remoteMapRootPath, userName)
	createNewRemoteRootDir(userRemoteMapPath)
	print("拷贝用户: ", userName, "<<<")

	needCopyFileCount	 = 0
	totalCopyFileCount	= 0
	# 开始拷贝文件夹
	fl = getModifyFiles()
	# print(fl)
	print("开始拷贝修改文件 >>>")
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


def main():
	try:
		print("初始化 ... ")
		if not initGlobalInfo():
			return

		print("获取拷贝文件数据 >>> ")
		if not process():
			os.system("pause")
		else:
			os.system("pause")
	except Exception as e:
		print(e)
		print("-------------------------------------------------------------------")
		print("--------------------------执行异常！ 找程序------------------------")
		print("-------------------------------------------------------------------")
		os.system("pause")

main()
