#! python3
# encoding: utf8
## python 版本3.x
## 支持配置 config.ini
import os, io, shutil
import errno, sys, traceback
import time, logging, json
import configparser, redis
from git import Git, Repo, util
from enum import Enum

# 基础配置
projectDir = r"../"
project = False
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
batPathParams = {}
batCopyPaths = {}

# 用户远端拷贝地址
userRemoteConfigPath	= ""
userRemoteMapPath		= ""

# 文本日志
logger = logging.getLogger()

# 文件类型枚举
class CopyType(Enum):
	invalid		= -1
	config 		= 1
	mapJson 	= 2
	mapNavmesh 	= 3

class MyRedis(object):
	def __init__(self, host, port, password, db):
		self.host = host
		self.port = port
		self.password = password
		self.db = db
		self.handle = False
		self.valid  = False

	def connect_redis(self):
		if self.handle:
			self.handle = False

		self.handle = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password, encoding='utf8')
		try:
			self.handle.ping()
			self.valid = True
			return self.isValid()
		except redis.exceptions.RedisError as e:
			log("connect_redis error %s", e)
			log("-------------------------------------------------------------------")
			log("---------------------- redis连接失败！！！------------------------")
			log("-------------------------------------------------------------------")
			self.valid = True
			return self.isValid()

	def isValid(self):
		return self.valid

	def get(self, key):
		if self.isValid():
			return self.handle.get(key)
		else:
			return False

	def set(self, key, value, ex):
		if self.isValid():
			return self.handle.set(key, value, ex=ex)
		else:
			return False

	def hset(self, name, key, value):
		if self.isValid():
			return self.handle.hset(name, key, value)
		else:
			return False

	def hget(self, name, key):
		if self.isValid():
			return self.handle.hget(name, key)
		else:
			return False

	def hgetall(self, name):
		if self.isValid():
			return self.handle.hgetall(name)
		else:
			return False

	def expire(self, name, time):
		if self.isValid():
			return self.handle.expire(name, time)
		else:
			return False


# 日志打印
def log(format, *args):
	global logger

	logger.critical(format, *args)

# 初始化日志系统
def initLogSys():
	global logger

	formatter = logging.Formatter('[%(asctime)s] %(message)s')
	fileHandler = logging.FileHandler('copy.log', mode='w', encoding='UTF-8')
	fileHandler.setLevel(logging.CRITICAL)
	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)
	logger.setLevel(logging.CRITICAL)
	consoleHandler = logging.StreamHandler()
	consoleHandler.setLevel(logging.CRITICAL)
	consoleHandler.setFormatter(formatter)
	logger.addHandler(consoleHandler)

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
			globalUserName = (config['COMMON']['globalUserName'].lower() == "true")

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
		log("%s is invalid dir", remoteConfigRootPath)
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
		project = Repo(projectDir)
	else:
		log("%s is invalid git repo", projectDir)
		return False

	return True

# 获取用户名称
def getUserName():
	global project
	global globalUserName
	
	if globalUserName:
		config = project.config_reader('global')
		return config.get("user", "name")
	else:
		config = project.config_reader('repository')
		return config.get("user", "name")

def _getModifyFiles():
	"""
		获取为推送的文件
		return: list
	"""
	global project
	fl = []
	for item in project.tree().diff(None):
		fl.insert(0, item.a_path)
		# a = item.a_rawpath.decode('unicode_escape').encode('unicode_escape')
		# print("a", a, type(a))
		# # print("1 ", item.a_rawpath.translate(None))
		# # break
	return fl

def _getUntrackFiles():
	"""
		获取未跟踪的文件
		return: list
	"""
	global project
	return project.untracked_files

# 删除目录
def rmOldRemoteRootDir(rootDir):
	if os.path.exists(rootDir):
		shutil.rmtree(rootDir)

# 生成远端根目录
def genRemoteDir(mod):
	global userRemoteConfigPath
	global userRemoteMapPath
	# 根据用户名创建新的远程文件夹
	userName = getUserName()
	userRemoteConfigPath = str.format(r"{}/{}", remoteConfigRootPath, userName)
	userRemoteMapPath 	 = str.format(r"{}/{}", remoteMapRootPath, userName)
	if mod != '4':
		rmOldRemoteRootDir(userRemoteConfigPath)
		rmOldRemoteRootDir(userRemoteMapPath)

	if mod != '4' and mod != '2':
		# 模式2不创建，是因为shutil.copytree需要目标文件目录不存在
		os.mkdir(userRemoteConfigPath)
		os.mkdir(userRemoteMapPath)

	log("拷贝用户: %s <<<", userName)

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
	log("拷贝 %s -> %s", filePath, remotePath)
	remoteDir = os.path.dirname(remotePath)
	try:
		os.makedirs(remoteDir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			log("copyOneFile create dir erorr! %s", os.strerror(e.errno))
			return False
	shutil.copy(filePath, remotePath)

	return True

def writeCopyCountToFile(mod, count):
	global userRemoteConfigPath

	fn = str.format("{}/count.txt", userRemoteConfigPath)
	f = open(fn, "w", encoding="utf-8")
	if f:
		f.write(str.format("{}\n{}", mod, count))
		f.close()
# 根据路径获取rediskey
def getRedisKeyByPath(relativePath):
	return relativePath.replace('/', '').replace('.', '')

# 记录修改信息
def recodeModifyInfoToRedis(modifys):
	curtime = time.time()
	deltime = 30 * 24 * 3600
	userName = getUserName()
	rd = MyRedis("192.168.10.81", 19000, 'nysy', '10')
	if not rd.connect_redis():
		return

	for filepath in modifys:
		redisHkey = getRedisKeyByPath(filepath)
		if rd.hset(redisHkey, userName, curtime) is False:
			log("error recodeModifyInfoToRedis hset %s: %s", filepath, userName)
		if rd.expire(redisHkey, deltime) is False:
			log("error recodeModifyInfoToRedis expire %s: %d", filepath, deltime)

# 根据远程文件名获取redis key
def getRedisKeyByRemotePath(remotePath):
	global userRemoteConfigPath
	global userRemoteMapPath
	if remotePath.find(userRemoteConfigPath) >= 0:
		remotePath = remotePath.replace(userRemoteConfigPath, '')
	elif remotePath.find(userRemoteMapPath) >= 0:
		remotePath = remotePath.replace(userRemoteMapPath, '')

	return getRedisKeyByPath(remotePath.replace('\\', '/'))

# 根据秒获取日期
def getDateInfo(t):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

# 检测修改者
def checkModifyUser(localToRemote):
	curtime = time.time()
	deltime = 30 * 24 * 3600
	rd = MyRedis("192.168.10.81", 19000, 'nysy', '10')
	if not rd.connect_redis():
		return

	uncommites = getModifyFiles()
	untrackedfile = _getUntrackFiles()
	for lfs in uncommites:
		untrackedInfo = ""
		if lfs in untrackedfile:
			untrackedInfo = "未跟踪文件: "
		lfs = lfs.replace('/', '\\')
		if localToRemote.get(lfs):
			rf = localToRemote[lfs]
			rk = getRedisKeyByRemotePath(rf)
			minfo = str.format("{}{} 修改记录:", untrackedInfo, lfs)
			for k, v in rd.hgetall(rk).items():
				t = float(v)
				if curtime < t + deltime:
					minfo = str.format("{} {}({});", minfo, k.decode('utf8'), getDateInfo(t))
			log(minfo)

# 根据文件列表拷贝到对应目录
def copyFileByList(fl):
	global userRemoteConfigPath
	global userRemoteMapPath
	needCopyFileCount 	= 0
	totalCopyFileCount	= 0
	recodeFiles = []
	for filePath in fl:
		filePath = str.format("{}/{}", projectDir, filePath)
		_copyType, relativePath = checkNeedCopy(filePath)
		if _copyType != CopyType.invalid:
			recodeFiles.append(relativePath)
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
			remoteFilePath = remoteFilePath.replace(".bin", ".bytes")

		log("%s %s", filePath, remoteFilePath)
		if remoteFilePath != "" and copyOneFile(filePath, remoteFilePath):
			totalCopyFileCount = totalCopyFileCount + 1

	if totalCopyFileCount != needCopyFileCount:
		log("-------------------------------------------------------------------")
		log("----------------------拷贝文件异常！！！！！-----------------------")
		log("-------------------------------------------------------------------")
		return False
	else:
		writeCopyCountToFile("modify", totalCopyFileCount)
		log("-------------------------------------------------------------------")
		log("----------------------------拷贝成功-------------------------------")
		log("-------------------------------------------------------------------")
		recodeModifyInfoToRedis(recodeFiles)
		return True

# 获取修改的文件列表 新增文件列表
def getModifyFiles():
	global project
	# 返回文件列表
	return _getModifyFiles() + _getUntrackFiles()

# 拷贝对应的修改文件 未commit的文件
def processModify():
	# 开始拷贝文件夹
	fl = getModifyFiles()
	return copyFileByList(fl)


# 拷贝全文件
def processCopyAll():
	global userRemoteConfigPath
	global userRemoteMapPath
	
	srcCount	= 0		# 源的文件数量
	copyCount 	= 0		# 拷贝的文件数量

	# 全拷贝配置
	configDir = str.format("{}/{}", projectDir, configCheckPath)
	shutil.copytree(configDir, userRemoteConfigPath)
	for root, dirs, files in os.walk(configDir):
		srcCount = srcCount + len(files)

	for root, dirs, files in os.walk(userRemoteConfigPath):
		copyCount = copyCount + len(files)

	# 全拷贝地图
	mapJsonDir = str.format("{}/{}", projectDir, mapJsonCheckPath)
	remoteJsonDir = str.format("{}/mapEditData", userRemoteMapPath)
	shutil.copytree(mapJsonDir, remoteJsonDir)

	for root, dirs, files in os.walk(mapJsonDir):
		srcCount = srcCount + len(files)

	for root, dirs, files in os.walk(remoteJsonDir):
		copyCount = copyCount + len(files)

	mapNavmeshDir = str.format("{}/{}", projectDir, mapNavmeshCheckPath)
	remoteNavmeshDir = str.format("{}/navmeshFile", userRemoteMapPath)

	for root, dirs, files in os.walk(mapNavmeshDir):
		for f in files:
			if os.path.splitext(f)[-1] == ".bin":
				srcCount = srcCount + 1
				filePath = str.format("{}/{}", mapNavmeshDir, f)
				remotePath = str.format("{}/{}", remoteNavmeshDir, f).replace(".bin", ".bytes")
				if copyOneFile(filePath, remotePath):
					copyCount = copyCount + 1

	if copyCount == srcCount:
		writeCopyCountToFile("all", copyCount)
		log("-------------------------------------------------------------------")
		log("----------------------------拷贝成功-------------------------------")
		log("-------------------------------------------------------------------")
	else:
		log("-------------------------------------------------------------------")
		log("----------------------------拷贝失败-------------------------------")
		log("-------------------------------------------------------------------")

# 根据提交SHA-1找出修改文件
def getCommitFileBySHA(sha):
	if len(sha) < 10:
		return False

	global project
	try:
		dl = project.commit(sha).stats.files
		fl = []
		for fp in dl:
			fl.append(fp)

		return fl
	except Exception as e:
		return False


# 根据提交文件内容拷贝
def processCommit():
	sha = input("请输入提交ID\n提交ID在git log中查看93cc057eb2 或者工具showlog中 SHA-1)\n")
	# sha = "40d09b7cb2387577a6d05ce56a26e618cdc0b946"
	fl = False
	while not fl:
		fl = getCommitFileBySHA(sha)
		if not fl:
			sha = input("请输入正确的提交ID\n")

	log("输入的SHA-1: %s", sha)
	return copyFileByList(fl)
# -------------------------------------------------------------------------------------------
# 从远端拷贝到内网
# -------------------------------------------------------------------------------------------
# 获取文件拷贝地址
def getFileCopyPaths(filePath):
	global userRemoteConfigPath
	global userRemoteMapPath
	global batCopyPaths
	tfp 	= filePath
	isDir 	= False
	fn 		= ""
	while True:
		if tfp == userRemoteConfigPath or tfp == userRemoteMapPath:
			return []
		elif batCopyPaths.get(tfp):
			if isDir:
				files = []
				for d in batCopyPaths[tfp]:
					files.append(str.format(r"{}\{}", d, fn))
				return files
			else:
				return batCopyPaths[tfp]
		else:
			if isDir:
				fn = str.format(r"{}\{}", os.path.basename(tfp), fn)
			else:
				fn = os.path.basename(tfp)
			tfp 	= os.path.dirname(tfp)
			isDir 	= True

# 解析批处理文件
def praseConfigBat():
	log("解析拷贝文件 >>")
	global userRemoteConfigPath
	global userRemoteMapPath
	global batPathParams
	global batCopyPaths
	f = open(str.format(r"../../{}", serverBatFileName), "r")
	for k in f.readlines():
		infos = k.split(" ")
		if infos[0] == "@set":
			kv = infos[1].split("=")
			if kv[0] == "remote_path" or kv[0] == "remote_map":
				batPathParams["remote_path"] = userRemoteConfigPath
				batPathParams["remote_map"] = userRemoteMapPath
			else:
				batPathParams[kv[0]] = str.format(r"{}/{}", projectDir, kv[1][3:-1])
		elif infos[0] == "copy":
			remote = infos[2][1:-1].split("%")
			remote = str.format("{}{}", batPathParams[remote[1]], remote[2])
			local  = infos[3][1:-2].split("%")
			local = str.format("{}{}", batPathParams[local[1]], local[2])
			remote.replace('/', '\\')
			if remote not in batCopyPaths:
				batCopyPaths[remote] = []
			batCopyPaths[remote].append(local)
	f.close()
	# log("批处理文件解析结果: %s", batCopyPaths)

def copyRemoteConfigToServer():
	global userRemoteConfigPath
	global userRemoteMapPath
	global batCopyPaths
	global projectDir
	praseConfigBat()
	
	remoteCount = -1
	remoteFiles = []
	tryCount 	= 0
	isCopyAll	= False
	while len(remoteFiles) != remoteCount:
		countfile = open(str.format(r"{}\count.txt", userRemoteConfigPath), 'r')
		if not countfile:
			log("拷贝数据记录count.txt文件不可访问")
			return

		s = countfile.read()
		countfile.close()
		info = s.split('\n')
		remoteCount = int(info[1])
		if info[0] == 'all':
			isCopyAll = True

		remoteFiles.clear()
		for d, r, fl in os.walk(userRemoteConfigPath):
			for f in fl:
				if f != "count.txt":
					fp = str.format(r"{}\{}", d, f)
					remoteFiles.append(fp)

		for d, r, fl in os.walk(userRemoteMapPath):
			for f in fl:
				fp = str.format(r"{}\{}", d, f)
				remoteFiles.append(fp)
		log("copyRemoteConfigToServer tryCount %d, remoteFilesLen %d, remoteCount %d", tryCount, len(remoteFiles), remoteCount)
		tryCount = tryCount + 1
		if tryCount > 30:
			log("请确认外网是否拷贝完成")
			return
		time.sleep(1)

	localToRemote = {}
	projectDirReplace = str.format(r"{}/", projectDir)
	for fp in remoteFiles:
		fs = getFileCopyPaths(fp)
		log("Remote File %s Server File %s", fp, fs)
		for lfs in fs:
			if copyOneFile(fp, lfs):
				localToRemote[lfs.replace(projectDirReplace, '')] = fp

	log("-------------------------------------------------------------------")
	log("-----------------------  拷贝结束！！！  ------------------------")
	log("-------------------------------------------------------------------")
	if isCopyAll:
		checkModifyUser(localToRemote)


def main():
	global userRemoteConfigPath
	global userRemoteMapPath
	global projectDir

	try:
		initLogSys()
		log("初始化 ... ")
		if not initGlobalInfo():
			return

		cmod = '1'
		if len(sys.argv) >= 2:
			cmod = sys.argv[1]

		genRemoteDir(cmod)

		if userRemoteConfigPath == "" or userRemoteMapPath == "" :
			log("-------------------------------------------------------------------")
			log("-------------------------远端地址异常------------------------------")
			log("-------------------------------------------------------------------")
			return

		if cmod == '1':
			log("开始拷贝修改配置 >>> ")
			processModify()
		elif cmod == '2':
			log("开始拷贝全部配置 >>> ")
			processCopyAll()
		elif cmod == '3':
			log("开始拷贝提交配置 >>> ")
			processCommit()
		elif cmod == '4':
			log("开始拷贝配置 >>> ")
			copyRemoteConfigToServer()
		else:
			log("-------------------------------------------------------------------")
			log("-----------------------启动参数异常！ 找程序------------------------")
			log("-------------------------------------------------------------------")
	except (KeyboardInterrupt,EOFError):
		pass
	except Exception as e:
		log(traceback.format_exc())
		log("-------------------------------------------------------------------")
		log("--------------------------执行异常！ 找程序------------------------")
		log("-------------------------------------------------------------------")
	finally:
		os.system("pause")

main()