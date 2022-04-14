import csv
import time
from csv import DictWriter
from datetime import datetime
from os import startfile
from sys import platform
from typing import TextIO

import psutil
from psutil import Process

platform_of_file = platform
header_memory1 = 'memory_info_wset' if platform_of_file == "win32" else 'memory_info_rss'
header_memory2 = 'memory_info_private' if platform_of_file == "win32" else 'memory_info_vms'


def writeheaderprocessing():
    csvfile: TextIO
    with open('log_proc.csv', "w", newline='') as csvfile:
        fieldnames = ['cpu_percent', 'num_open_files', header_memory1, header_memory2, 'log_timestamp']
        writer: DictWriter[str] = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def processing(pid):
    proc = psutil.Process(pid)

    csvfile: TextIO
    with open('log_proc.csv', "a", newline='') as csvfile:
        fieldnames = ['cpu_percent', 'num_open_files', 'memory_info_wset', 'memory_info_private', 'log_timestamp']
        writer: DictWriter[str] = csv.DictWriter(csvfile, fieldnames=fieldnames)

        date_memory1 = proc.memory_info().private if platform_of_file == "win32" else proc.memory_info().vms
        writer.writerow({'cpu_percent': proc.cpu_percent(interval=None),
                         'num_open_files': len(proc.open_files()),
                         header_memory1: proc.memory_info().rss,
                         header_memory2: date_memory1,
                         'log_timestamp': datetime.now()})


if __name__ != "__main__":
    pass
else:
    path_to_file: str = input("Insert path for file: ")
    name_of_file = path_to_file.rpartition('\\')[-1]
    log_timeout = int(input("Insert timeout for log: "))
    writeheaderprocessing()
    startfile(path_to_file)
    process: Process
    while True:
        for process in psutil.process_iter():
            cmdline = str(process.cmdline)
            if name_of_file in cmdline and "running" in cmdline:
                pid_of_file = process.pid
                processing(pid_of_file)
                time.sleep(log_timeout)
                break
