import sys,os,io,time, shutil, datetime

targetDir       = "f:/12121"
transferPath	= "C:/Users/dangxiaojie/Documents/Tencent Files/3289685120/Image"

def main():
    dt = datetime.datetime.strptime("2020-11-04 10:09:00", "%Y-%m-%d %H:%M:%S")
    # now = time.time()
    beginTime = dt.timestamp() - 60
    endTime   = dt.timestamp() + 60
    if not os.path.isdir(targetDir):
        try:
            os.makedirs(targetDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                log("create dir erorr! %s", os.strerror(e.errno))
                return False

    for r, d, files in os.walk(transferPath):
        for f in files:
            filepath = r + "/" + f
            mtime = os.path.getmtime(filepath)
            if mtime >= beginTime and mtime <= endTime :
                filename = os.path.basename(filepath)
                print(filepath)
                shutil.copy(filepath, targetDir + "/" + filename)

main()