#!/usr/bin/env python3

import os
import hashlib
import tempfile
import json
import time

hashfunc = hashlib.sha224

total_size = 0

def xprint(fd, inodes):
    os.write(fd, json.dumps(inodes, indent=4, sort_keys=True).encode('utf-8'))

def hash_file(name):
    xhash = hashfunc()
    with open(name, 'rb') as f:
        data = f.read(64*1024)
        while len(data) > 0:
            xhash.update(data)
            data = f.read(64*1024)
    return xhash.hexdigest(), xhash.name

def file_handler(path):
    digest, hash_name = hash_file(path)
    return digest, hash_name

def directory_handler(path):
    global total_size
    inodes = dict()
    for dirent in os.listdir(path):
        inode = dict()
        fullpath = "{}/{}".format(path, dirent)
        if os.path.isdir(fullpath):
            if dirent == ".backup":
                continue
            digest, hash_name = directory_handler(fullpath)
            inode[hash_name] = digest
        elif os.path.isfile(fullpath):
            digest, hash_name = file_handler(fullpath)
            inode[hash_name] = digest

        stat = os.lstat(fullpath)

        inode["mtime_ns"] = stat.st_mtime_ns
        inode["mode"] = stat.st_mode
        inode["uid"] = stat.st_uid
        inode["gid"] = stat.st_gid
        inode["size"] = stat.st_size
        inodes[dirent] = inode

        total_size += stat.st_size

    fd, tmpfile_name = tempfile.mkstemp(dir=".backup/tmp")
    xprint(fd, {"inodes" : inodes})
    os.close(fd)

    digest, hash_name = hash_file(tmpfile_name)
    os.rename(tmpfile_name, ".backup/blobs/{}".format(digest))
    return digest, hash_name

os.makedirs(".backup/blobs", exist_ok=True)
os.makedirs(".backup/tmp", exist_ok=True)

# Make a head pointer stored in .backup/head (which is actually a symlink)
root_blob, hash_name = directory_handler(".")
fd, tmpfile_name = tempfile.mkstemp(dir=".backup/tmp")
head = dict()
head['date'] = time.time()
head['root'] = {hash_name : root_blob}
xprint(fd, head)
os.close(fd)
digest, hash_name = hash_file(tmpfile_name)
head_filename = ".backup/blobs/{}".format(digest)
os.rename(tmpfile_name, head_filename)
try:
    os.remove(".backup/head.prev")
except:
    pass
try:
    os.rename(".backup/head", ".backup/head.prev")
except:
    pass
os.symlink("blobs/{}".format(digest), ".backup/head")

print("head", ".backup/head")
print("total_size", total_size)


