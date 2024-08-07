import sys, os, io, time, shutil, datetime, string

exts = [".gif", ".jpg", ".png", ".mp4", ".bmp"]
targetRoot = "f:/Pic"
imagePath = "C:/Users/dangxiaojie/Documents/Tencent Files/3289685120/nt_qq/nt_data"
# timestr = "2024-04-01 14:12:00"
interval = 20 * 60
findDirs = ["Pic", "Video"]


def processDir(pdir, beginTime, endTime, fileBase, beginIndex, targetDir):
    for r, d, files in os.walk(pdir):
        # print("r", os.path.basename(r))
        if os.path.basename(r) != "Ori":
            continue
        for f in files:
            filepath = r + "/" + f
            mtime = os.path.getmtime(filepath)
            # print("filepath: ", filepath, "mtime: ", mtime)
            # print("mtime >= beginTime: ", (mtime >= beginTime), "mtime <= endTime: ", (mtime <= endTime))
            if mtime >= beginTime and mtime <= endTime:
                filename = os.path.basename(filepath)
                ext = os.path.splitext(filename)[-1].lower()
                if ext in exts:
                    print(filepath)
                    beginIndex = beginIndex + 1
                    shutil.copy(
                        filepath, targetDir + "/" + fileBase +
                        "{:0>3d}".format(beginIndex) + ext)

    return beginIndex


def main():
    dt = datetime.datetime.now()

    if 'timestr' in globals().keys():
        dt = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

    targetDir = targetRoot + "/" + dt.strftime("%Y%m")
    fileBase = dt.strftime("%Y%m%d%H%M%S")
    beginTime = dt.timestamp() - interval
    endTime = dt.timestamp() + interval
    print("beginTime: ", beginTime, "endTime: ", endTime)
    if not os.path.isdir(targetDir):
        try:
            os.makedirs(targetDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                log("create dir erorr! %s", os.strerror(e.errno))
                return False

    # month_st = dt.strftime("%Y-%m")
    beginIndex = 0
    for _dir in findDirs:
        path_dir = imagePath + "/" + _dir
        print("path_dir", path_dir)
        beginIndex = processDir(path_dir, beginTime, endTime, fileBase,
                                beginIndex, targetDir)

    print("total: ", beginIndex)
    os.system("explorer.exe %s" % targetDir.replace("/", "\\"))


main()
