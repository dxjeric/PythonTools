import sys, os, zipfile, time

MAX_ZIP_FILE_SIZE = 1024 * 1024 * 1024 * 20
RM_AFTER_ZIP = False


def main():
    print("sys.argv: ", len(sys.argv), str(sys.argv[0]))
    dirPath = str(sys.argv[1])
    all_books = []

    maxZipFileSize = -1
    if 'MAX_ZIP_FILE_SIZE' in globals().keys():
        maxZipFileSize = MAX_ZIP_FILE_SIZE

    if dirPath[-1] == '/':
        dirPath = dirPath[0:-1]

    os.system("mv {} ./".format(dirPath))
    zipBase = os.path.basename(dirPath)
    print("dirPath", dirPath, "maxZipFileSize", maxZipFileSize)
    for r, _, files in os.walk(zipBase):
        for f in files:
            all_books.append(r + "/" + f)

    print("len(all_books)", len(all_books), "begin", time.time())
    logfile = open(zipBase + ".txt", "w")
    partIndex = 0
    bookIndex = 0
    totalFileCount = 0
    allZipFileNames = []
    while bookIndex < len(all_books):
        partIndex += 1
        totalSize = 0
        zipfillename = r'{}.part{:0>2d}.zip'.format(zipBase, partIndex)
        if maxZipFileSize == -1:
            zipfillename = r'{}.zip'.format(zipBase)
        allZipFileNames.append(zipfillename)
        zipFile = zipfile.ZipFile(zipfillename, 'w')
        curZipFileCount = 0
        while bookIndex < len(all_books) and (maxZipFileSize == -1
                                              or totalSize < maxZipFileSize):
            totalFileCount += 1
            curZipFileCount += 1
            fp = all_books[bookIndex]
            bookIndex += 1
            stats = os.stat(fp)
            totalSize += stats.st_size
            zipFile.write(fp, fp, zipfile.ZIP_DEFLATED)
            if RM_AFTER_ZIP:
                os.remove(fp)  # 删除文件
        zipFile.close()
        log_str = "zipfillename: {},  curZipFileCount: {}, totalFileCount: {}".format(
            zipfillename, curZipFileCount, totalFileCount)
        logfile.write(log_str)
        print(log_str)

    logfile.write("\n\n")
    logfile.close()
    print("zip ok! begin md5sum!", "time: ", time.time())
    os.system("md5sum {}.part0*.zip >> {}.txt".format(zipBase, zipBase))
    os.system("echo zip md5sum finish! >> {}.txt".format(zipBase))
    os.system("rm -fr {}".format(zipBase))
    print("finsh totalFileCount: ", totalFileCount, "end", time.time())


if __name__ == "__main__":
    main()
