#! python3
# #coding=utf-8
import psutil
import sys
import time
import asyncio
import io
import tkinter as tk
import signal

is_sigint_up = False
def sigint_handler(signum, frame):
  global is_sigint_up
  is_sigint_up = True
  print('catched interrupt signal!')

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

async def main():
    wfile = open("cpu.txt", "w", encoding='utf-8')
    while 1:
        if is_sigint_up:
            wfile:close()
            return
        else:
            await asyncio.sleep(1)
            _time = time.time()
            for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
                procStr = str.format("{},{},{},{}\n", _time, proc.info['pid'], proc.info['name'], proc.info['cpu_percent'])
                wfile.write(procStr)
                wfile.flush()




asyncio.run(main())