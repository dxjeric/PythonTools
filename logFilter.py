# encoding: utf8
import sys,os,io
import chardet

filterLogFiles = ["centerserver.log", "gameserver.log", "gateserver.log", "loginserver.log", "worldserver.log"]
filterLogDir = "E:/log/180723143145"

uniqErrorsStack     = []    # 代码堆栈信息
uniqErrorsFirstLine = []    # 日志第一行信息 相同的堆栈信息的第一行会拼接起来
uniqErrorsNoPres    = []    # 除却前缀的信息 为了检索相同的信息

curErrorStack       = ""    # 当前报错的堆栈信息
curErrorFistLine    = ""    # 当前报错的第一行
curErrorNoPres      = ""    # 当前报错的非堆栈信息 除去前缀

def addNewError():
    if curErrorStack == "":
        return

    global uniqErrorsStack
    global uniqErrorsFirstLine
    global uniqErrorsNoPres
    global curErrorNoPres
    if curErrorStack not in uniqErrorsStack:
        uniqErrorsStack.append(curErrorStack)
        uniqErrorsFirstLine.append(curErrorFistLine)
        uniqErrorsNoPres.append(curErrorNoPres)
    elif curErrorNoPres not in uniqErrorsNoPres:
        uniqErrorsNoPres.append(curErrorNoPres)
        i = uniqErrorsStack.index(curErrorStack)
        uniqErrorsFirstLine[i] += curErrorFistLine

def filterOneError(oneLine):
    global curErrorStack    
    global curErrorFistLine
    global curErrorNoPres
    plusIndex = oneLine.find("+++")
    if plusIndex == -1:
        plusIndex = oneLine.find("<<<")
    
    if plusIndex == -1:
        return

    if plusIndex == 0 :
        curErrorStack += oneLine
    else:
        addNewError()
        curErrorStack       = ""
        curErrorFistLine    = oneLine
        curErrorNoPres      = oneLine[plusIndex:]

        

def processOneLogFile(fileName):
    global uniqErrorsStack
    global uniqErrorsFirstLine

    if not os.path.exists(fileName):
        return
    
    print("processOneLogFile", fileName)
    fh = open(fileName, "r", encoding="utf-8")
    for line in fh.readlines():
        filterOneError(line)
    addNewError()
    fh.close()
    
    dotIndex = fileName.rfind(".")
    if dotIndex == -1:
        wfn = fileName + ".filter.txt"
    else:
        wfn = fileName[0:dotIndex] + ".filter" + fileName[dotIndex:]

    wf = open(wfn, "w", encoding="utf-8")
    for index in range(len(uniqErrorsStack)):
        wf.write(uniqErrorsFirstLine[index])
        wf.write(uniqErrorsStack[index])
        wf.write("\n")

    wf.close()
    uniqErrorsStack.clear()
    uniqErrorsFirstLine.clear()
    uniqErrorsNoPres.clear()


def processOneDir(dirName):
    for fn in filterLogFiles:
        processOneLogFile(dirName + "/" + fn)


def main():
    # 先处理根目录中的文件
    processOneDir(filterLogDir)

    # 处理子目录文件
    for root, dirs, files in os.walk(filterLogDir):
        for dirName in dirs:
            processOneDir(root+ "/" + dirName)
        


main()