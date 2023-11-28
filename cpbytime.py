import sys,os,io,time, shutil, datetime

exts        = [".gif", ".jpg", ".png", ".mp4", ".bmp"]
targetRoot  = "f:/Pic"
imagePath	= "C:/Users/dangxiaojie/Documents/Tencent Files/3289685120"
#timestr     = "2023-11-28 09:55:00"
interval    = 5*60


def processDir(pdir, beginTime, endTime, fileBase, beginIndex, targetDir):
    for r, d, files in os.walk(pdir):
        for f in files:
            filepath = r + "/" + f
            mtime = os.path.getmtime(filepath)
#            print("filepath: ", filepath, "mtime: ", mtime)
#            print("mtime >= beginTime: ", (mtime >= beginTime), "mtime <= endTime: ", (mtime <= endTime))
            if mtime >= beginTime and mtime <= endTime :
                filename = os.path.basename(filepath)
                ext = os.path.splitext(filename)[-1].lower()
                if ext in exts:
                    print(filepath)
                    shutil.copy(filepath, targetDir + "/" + fileBase + "_" + str(beginIndex) + ext)
                    beginIndex = beginIndex + 1
    return beginIndex

def main():
    dt = datetime.datetime.now()

    if 'timestr' in globals().keys():        
        dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        
    targetDir = targetRoot + "/" + dt.strftime("%Y%m%d")
    fileBase = dt.strftime("%Y%m%d_%H%M%S")
    beginTime = dt.timestamp() - interval
    endTime   = dt.timestamp() + interval
    print("beginTime: ", beginTime, "endTime: ", endTime)
    if not os.path.isdir(targetDir):
        try:
            os.makedirs(targetDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                log("create dir erorr! %s", os.strerror(e.errno))
                return False

    beginIndex = processDir(imagePath, beginTime, endTime, fileBase, 0, targetDir)
    print("total: ", beginIndex)

main()