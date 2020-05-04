#!/usr/bin/env python3

import os
import hashlib
import tempfile
import json
import time

hashfunc = hashlib.sha224

total_size = 0
os.makedirs(".backup/blobs", exist_ok=True)
os.makedirs(".backup/tmp", exist_ok=True)

def xprint(fd, inodes):
    os.write(fd, json.dumps(inodes, indent=4, sort_keys=True).encode('utf-8'))

def root_to_filename(root):
    h = root[hashfunc().name]
    return ".backup/blobs/{}".format(h)

def load_root(root):
    if root:
        return json.load(open(root_to_filename(root), 'r'))
    return {}

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

def directory_handler(path, prev_root):
    global total_size
    inodes = dict()
    for dirent in os.listdir(path):
        fullpath = "{}/{}".format(path, dirent)
        if os.path.isdir(fullpath):
            if dirent == ".backup":
                continue
        stat = os.lstat(fullpath)
        inode = dict()
        inode["mtime_ns"] = stat.st_mtime_ns
        inode["mode"] = stat.st_mode
        inode["uid"] = stat.st_uid
        inode["gid"] = stat.st_gid
        inode["size"] = stat.st_size
        prev_inode = None
        if prev_root and 'inodes' in prev_root and dirent in prev_root['inodes']:
            prev_inode = prev_root['inodes'][dirent]
        if os.path.isdir(fullpath):
            pr = None
            if prev_root and 'inodes' in prev_root and dirent in prev_root['inodes']:
                pr = prev_root['inodes'][dirent]
            digest, hash_name = directory_handler(fullpath, load_root(pr))
            inode[hash_name] = digest
        elif os.path.isfile(fullpath):
            if prev_inode:
                if prev_inode["mtime_ns"] == stat.st_mtime_ns:
                    #print("skipping {}".format(fullpath))
                    inode = prev_inode
                else:
                    #print("mtime_ns check fail {}".format(fullpath))
                    digest, hash_name = file_handler(fullpath)
                    inode[hash_name] = digest
            else:
                #print("prev_inode check fail {}".format(fullpath))
                digest, hash_name = file_handler(fullpath)
                inode[hash_name] = digest

        inodes[dirent] = inode

        total_size += stat.st_size

    fd, tmpfile_name = tempfile.mkstemp(dir=".backup/tmp")
    xprint(fd, {"inodes" : inodes})
    os.close(fd)

    digest, hash_name = hash_file(tmpfile_name)
    target = ".backup/blobs/{}".format(digest)
    if os.path.exists(target):
        os.remove(tmpfile_name)
        #print("{} already exists for {}".format(target, path))
    else:
        os.rename(tmpfile_name, ".backup/blobs/{}".format(digest))
        #print("{} created for {}".format(target, path))
    return digest, hash_name

def make_backup(prev_root=None):
    # Make a head pointer stored in .backup/head (which is actually a symlink)
    root_blob, hash_name = directory_handler(".", load_root(prev_root))
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

if __name__ == "__main__":
    fp = None
    try:
        fp = open(".backup/head", "r")
    except FileNotFoundError:
        pass
    if fp:
        prev_backup = json.load(fp)
        make_backup(prev_backup['root'])
    else:
        make_backup()
    print("head", ".backup/head")
    print("total_size", total_size)

