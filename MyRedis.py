#! python3
# encoding: utf8

import redis, os, io, shutil, errno, sys, traceback, time, logging
import pytest


# 文本日志
logger = logging.getLogger()


# 日志打印
def log(format, *args):
	global logger
	logger.critical(format, *args)

# 初始化日志系统
def initLogSys(logName):
    global logger
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    fileHandler = logging.FileHandler(logName, mode='w', encoding='UTF-8')
    fileHandler.setLevel(logging.CRITICAL)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.CRITICAL)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.CRITICAL)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

class MyRedis(object):
    def __init__(self, host, port, password, db):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.handle = False
        self.valid  = False

    def connect_redis(self):
        if self.handle:
            self.handle = False
        self.handle = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password, encoding='utf8')
        try:
            self.handle.ping()
            self.valid = True
            return self.isValid()
        except redis.exceptions.RedisError as e:
            log("connect_redis error %s", e)
            self.valid = True
            return self.isValid()

    def isValid(self):
        return self.valid

    def get(self, key):
        if self.isValid():
            return self.handle.get(key)
        else:
            return False

    def set(self, key, value, ex):
        if self.isValid():
            return self.handle.set(key, value, ex=ex)
        else:
            return False
    
    def hget(self, name, key):
        if self.isValid():
            return self.handle.hget(name, key)
        else:
            return False

    def hgetall(self, name):
        if self.isValid():
            return self.handle.hgetall(name)
        else:
            return False
    
    def expire(self, name, time):
        if self.isValid():
            return self.handle.expire(name, time)
        else:
            return False


def main():
    old = {'a':1, 'b':2, 'c':5}
    delitems = []
    for k,v in old.items():
        if 5 > v:
            delitems.append(k)
    print(old)            
    # myredis = MyRedis("192.168.10.81", 19000, 'nysy', 15)
    # try:
    #     if myredis.connect_redis():
    #         print("1", myredis.get("acv"))
    # except Exception as e:
    #     print("e", e)

    # try:
    #     myredis.password = "nysy"
    #     if myredis.connect_redis():
    #         print("1", myredis.get("acv"))
    # except Exception as e:
    #     print("1111", e)
    
main()