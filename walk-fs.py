#!/usr/bin/env python3

import os
import hashlib
import tempfile

hashfunc = hashlib.sha224

total_size = 0

def xprint(fd, key=None, value=None):
    if key and value:
        os.write(fd, "{} {}\n".format(key, value).encode('utf-8'))
    else:
        os.write(fd, "\n".encode('utf-8'))

def hash_file(name):
    xhash = hashfunc()
    with open(name, 'rb') as f:
        data = f.read(64*1024)
        while len(data) > 0:
            xhash.update(data)
            data = f.read(64*1024)
    return xhash.hexdigest(), xhash.name

def directory_handler(path):
    global total_size
    fd, tmpfile_name = tempfile.mkstemp(dir=".backup")

    for dirent in os.listdir(path):
        fullpath = "{}/{}".format(path, dirent)
        if os.path.isdir(fullpath):
            if dirent == ".backup":
                continue
            directory_handler(fullpath)
        stat = os.lstat(fullpath)

        xprint(fd, "name", dirent)
        xprint(fd, "mtime_ns", stat.st_mtime_ns)
        xprint(fd, "mode", stat.st_mode)
        xprint(fd, "uid", stat.st_uid)
        xprint(fd, "gid", stat.st_gid)
        xprint(fd, "size", stat.st_size)

        if os.path.isfile(fullpath):
            digest, hash_name = hash_file(fullpath)
            xprint(fd, hash_name, digest)
        xprint(fd)
        total_size += stat.st_size
    os.close(fd)
    digest, hash_name = hash_file(tmpfile_name)
    os.rename(tmpfile_name, ".backup/{}".format(digest))
    return digest

os.makedirs(".backup", exist_ok=True)
print(".", directory_handler("."))
print("total_size", total_size)
