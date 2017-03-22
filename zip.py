# -*- coding: utf-8 -*-
import os,re, shutil, zipfile
import MoveOut as MvOut

zipFileName = "./appConfig.zip".decode('utf8').encode('GBK')
ftpPath = "沙鹰/Out"

def zip_dir():
	zf = zipfile.ZipFile(zipFileName, "w", zipfile.zlib.DEFLATED)
	for root, dirs, files in os.walk(r"./out"):
		for f in files:
			fullpath = os.path.join(root, f)
			arname = fullpath[len(r"./out"):]
			zf.write(fullpath, arname)
	zf.close()

def SynConfig():
	zip_dir()
	# ftp = MvOut.connect()
	# ftp.cwd(ftpPath.decode('utf8').encode('GBK'))
	# MvOut.upload(ftp, zipFileName)
	# MvOut.disconnect(ftp)

SynConfig()
print(u'转换完毕')