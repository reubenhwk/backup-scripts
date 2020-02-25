#!/usr/bin/env python3

import os
import hashlib

hashfunc = hashlib.sha224

total_size = 0

def directory_handler(path):
    global total_size
    for dirent in os.listdir(path):
        try:
            fullpath = "{}/{}".format(path, dirent)
            stat = os.lstat(fullpath)
            if os.path.isdir(fullpath):
                directory_handler(fullpath)
            print("name", dirent)
            print("mtime_ns", stat.st_mtime_ns)
            print("mode", stat.st_mode)
            print("uid", stat.st_uid)
            print("gid", stat.st_gid)
            print("size", stat.st_size)
            if os.path.isfile(fullpath):
                xhash = hashfunc()
                with open(fullpath, 'rb') as f:
                    data = f.read(64*1024)
                    while len(data) > 0:
                        xhash.update(data)
                        data = f.read(64*1024)
                digest = xhash.hexdigest()
                print(xhash.name, digest)
            print()
            total_size += stat.st_size
        except:
            print("--> error", fullpath)

directory_handler(".")
print("total_size", total_size)
