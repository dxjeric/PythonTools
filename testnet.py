# python3
# encoding: utf8

import sys
import socket
import asyncio

totalCount = 0
def createNewConnectTest(host, port):
    global totalCount
    print("createNewConnectTest")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error socket: %s" % e)
        return

    try:
        s.connect((host, port))
    except socket.error as e:
        print("Error connect socket: %s" % e)
        return

    try:
        s.close()
        totalCount = totalCount + 1
        print("createNewConnectTest close", totalCount)
    except socket.error as e:
        print("Error close socket: %s" % e)
        return



async def main():
    while 1:
        await asyncio.sleep(2)
        count = 10
        while count > 0:
            createNewConnectTest("192.168.4.108", 9031)
            count = count - 1

asyncio.run(main())