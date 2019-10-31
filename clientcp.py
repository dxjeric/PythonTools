#! python3
# #coding=utf-8
import sys, time, msvcrt, shutil, os

defaultPath = r"\\192.168.10.11\share\2号_Release\windows\nysy_windows_syyx-6.0.1000.zip"
def readKeyBoardInput(timeout = 5):
    start_time = time.time()
    sys.stdout.write("输入拷贝地址，" + str(timeout) + "秒不输入则使用默认值\n")
    sys.stdout.flush()
    inputPath = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getwch()
            sys.stdout.write(chr)
            sys.stdout.flush()
            # print("char", chr, ord(chr), str(chr))
            # if ord(chr) == 27: # ESC
            #     break
            if ord(chr) == 13: # Enter
                break
            inputPath = inputPath  + str(chr)
        if len(inputPath) == 0 and (time.time() - start_time) > timeout:
            break
    if len(inputPath) == 0:
        return defaultPath
    else:
        return inputPath

def main():
    srcpath = readKeyBoardInput()
    print('拷贝路径:%s' % srcpath)
    dirpath, filename = os.path.split(srcpath)
    destpath = os.path.join(r'C:\Users\chengxu12\Desktop', filename)
    if os.path.exists(srcpath):
        shutil.copyfile(srcpath, destpath)
    else:
        print("文件不存在", srcpath)
    
    # 解压文件
    print("解压文件")
    cmd = "\"c:\\Program Files (x86)\\HaoZip\\HaoZipC.exe\" x " + destpath + " -aoa -o" + "C:\\Users\\chengxu12\\Desktop\\clients"
    os.system(cmd)
    print("删除文件")
    os.remove(destpath)
    os.system(r"explorer.exe C:\Users\chengxu12\Desktop\clients\nysy_windows_syyx")

main()