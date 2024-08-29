import os, sys


def main():
    path = os.getcwd()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        path = path.replace("/cygdrive/", "").replace("/", "\\")
        path = path[0:1] + ":" + path[1:]

    os.system("start explorer %s" % path)


main()
