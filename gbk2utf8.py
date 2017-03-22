# encoding: utf8

import sys,os,ftplib,socket,io

transferFileExt 	= ["txt"]
transferPath		= "./"

def main():
	for r, d, files in os.walk(transferPath):
		for f in files:
			if f.split('.')[-1] in transferFileExt :
				filepath = r + "/" + f
				print(filepath)
				file_r = io.open(filepath, "rb")
				rd = file_r.read()
				file_r.close()
				try:
					wd = rd.decode('gbk').encode('utf8')
				except:
					wd = rd

				file_w = io.open(filepath, 'wb')
				file_w.write(rd.decode('gbk').encode('utf8'))
				file_w.close()

main()