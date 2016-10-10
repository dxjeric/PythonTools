# encoding: utf8

import sys,os

ConstShaYingFiles = ['py']
gbkGang = str('/').decode('utf8')

def renameFile(root, fileName):	
	fileInfos 	= fileName.split('.')	
	if len(fileInfos) < 2 or fileInfos[1] in ConstShaYingFiles:
		return
	#print(root.decode('GBK'), fileName.decode('GBK'), gbkGang)
	root 		= root.decode('GBK')
	fileExt 	= fileInfos[1].decode('GBK')
	reName		= fileInfos[0].decode('GBK').split('@')[0]	
	oldName = root + gbkGang + fileName.decode('GBK')
	newName = root + gbkGang + reName + "." + fileExt
	if not os.path.exists(newName):
		os.rename(oldName, newName)
	else:
		err = str("重命名的文件已经存在: ").decode('utf8').encode('GBK') + oldName.encode('GBK')
		print(err)


def traverseDir(dir):
	for r, d, files in os.walk(dir):
		for f in files:
			renameFile(r, f)

		for dd in d:
			newDir = r + "/" + dd
			traverseDir(newDir)


def main():
	try:
		rootDir = raw_input(str("输入要转换的路径: ").decode('utf8').encode('GBK'))
		traverseDir(rootDir)
		raw_input(str("按回车退出程序...").decode('utf8').encode('GBK'))
	except:
		return		


main()