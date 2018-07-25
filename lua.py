# encoding: utf8

import sys,os

constLen = len("E:\\GitHub\\behaviac-lua") + 1
hasadd = []


def traverseDir(dir):
	for r, d, files in os.walk(dir):
		for f in files:
			fileInfos = f.split('.')
			if fileInfos[-1] == "lua" :
				s = r + "/" + f
				s = s.replace("/", ".")
				s = s.replace("\\", ".")
				k = "d_"+fileInfos[0]
				if k not in hasadd:
					hasadd.append( k)
					print(k + " = require \"" + s[constLen:-4] + "\"")
	
		for dd in d:
			if dd != ".git":
				newDir = r + "/" + dd
				traverseDir(newDir)


def main():
		traverseDir("E:\\GitHub\\behaviac-lua")	


main()