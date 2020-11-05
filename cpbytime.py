import sys,os,io,time, shutil, datetime

targetDir   = "f:/12121"
imagePath	= "C:/Users/dangxiaojie/Documents/Tencent Files/3289685120"
# videoPath   = "C:/Users/dangxiaojie/Documents/Tencent Files/3289685120/Video"
timestr     = "2020-11-05 11:37:38"
interval    = 60 * 1

def processDir(pdir, beginTime, endTime, fileBase, beginIndex):
    for r, d, files in os.walk(pdir):
        for f in files:
            filepath = r + "/" + f
            mtime = os.path.getmtime(filepath)
            if mtime >= beginTime and mtime <= endTime :
                filename = os.path.basename(filepath)
                ext = os.path.splitext(filename)[-1]
                print(filepath)
                shutil.copy(filepath, targetDir + "/" + fileBase + "_" + str(beginIndex) + ext)
                beginIndex = beginIndex + 1
    return beginIndex

def main():
    dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    fileBase = dt.strftime("%Y%m%d_%H%M%S")
    beginTime = dt.timestamp() - interval
    endTime   = dt.timestamp() + interval
    if not os.path.isdir(targetDir):
        try:
            os.makedirs(targetDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                log("create dir erorr! %s", os.strerror(e.errno))
                return False

    beginIndex = processDir(imagePath, beginTime, endTime, fileBase, 0)

main()