import sys, os, hashlib, zipfile

MAX_ZIP_FILE_SIZE = 1024 * 1024

def getFileMd5Str(file_path):
    with open(file_path, "rb") as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5str = md5obj.hexdigest()
        return str(md5str).upper()

def main():
    print("sys.argv: ", len(sys.argv), str(sys.argv[0]))
    dirPath = str(sys.argv[1])    
    all_books = []

    maxZipFileSize = -1
    if 'MAX_ZIP_FILE_SIZE' in globals().keys():
        maxZipFileSize = MAX_ZIP_FILE_SIZE
    
    if dirPath[-1] == '/':
        dirPath = dirPath[0:-1]
    
    print("dirPath", dirPath, "maxZipFileSize", maxZipFileSize)
    for r, _, files in os.walk(dirPath):
        for f in files:
            all_books.append(r + "/" + f)
    
    # print("all_books: ", all_books, "len(all_books)", len(all_books))
    zipBase = os.path.basename(dirPath)
    logfile = open(zipBase + ".txt", "w")    
    partIndex = 0
    bookIndex = 0
    totalFileCount = 0
    allZipFileNames = []
    while bookIndex < len(all_books):
        partIndex += 1
        totalSize = 0
        zipfillename = r'{}.part{:0>2d}.zip'.format(zipBase, partIndex)
        if maxZipFileSize == -1 : 
            zipfillename = r'{}.zip'.format(zipBase)
        allZipFileNames.append(zipfillename)
        zipFile = zipfile.ZipFile(zipfillename, 'w')
        curZipFileCount = 0
        while bookIndex < len(all_books) and (maxZipFileSize == -1 or totalSize < maxZipFileSize):
            totalFileCount += 1
            curZipFileCount += 1
            fp = all_books[bookIndex]
            bookIndex += 1            
            stats = os.stat(fp)
            totalSize += stats.st_size
            zipFile.write(fp, fp, zipfile.ZIP_DEFLATED)
        logfile.write("file name: {},  zip file: {}, total: {}\n".format(zipfillename, curZipFileCount, totalFileCount))
        print("curZipFileCount:", curZipFileCount, "totalFileCount:", totalFileCount, "totalSize:", totalSize, "maxZipFileSize:", maxZipFileSize)
        zipFile.close()
    logfile.write("\n\n")
    logfile.close()
    os.system("md5sum {}.part0*.zip >> {}.txt".format(zipBase, zipBase))
    print("finsh totalFileCount: ", totalFileCount)    

if __name__ == "__main__":
	main()    