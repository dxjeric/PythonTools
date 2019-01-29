#! python3
# encoding: utf8
import sys,os,io

fileInfos     = []      # 需要转换的文件信息
filelineinfo  = {}      # 整理过的数据

def processFileInfos():
    global fileInfos
    global filelineinfo
    for line in fileInfos:
        if line == ' ':
            continue
        
        ps = line.split(',')
        if len(ps) != 6:
            continue
        
        filename = ps[4][1:]
        fileline = int(ps[5])
        if filename not in filelineinfo:
            filelineinfo[filename] = [[], []]

        filelineinfo[filename][0].append(fileline)
        filelineinfo[filename][1].append(line)


def gen(filepath):
    global filelineinfo
    filepath += ".csv"
    wh = open(filepath, "w", encoding='utf-8')
    for key, v in filelineinfo.items():
        if key.find(".lua") == -1 :
            continue
        
        print(key)
        luaf = open(key, "r", encoding='utf-8')
        lualines = luaf.readlines()
        luaf.close()
        al = len(v[0])
        lines = v[0]
        srclines = v[1]
        for i in range(al):
            ws = "\"" + lualines[lines[i]-1][0:-1] + "\""
            wh.write(ws)
            wh.write(",")
            wh.write(srclines[i])
    
    wh.close()

def doOneFile(filepath):
    global fileInfos
    fh = open(filepath, "r", encoding='utf-8')
    fileInfos = fh.readlines()
    fh.close()
    processFileInfos()
    fileInfos.clear()
    gen(filepath)


def main():
    doOneFile("./client03.csv")
    doOneFile("./client04.csv")
    # doOneFile("./server05.csv")
    


main()