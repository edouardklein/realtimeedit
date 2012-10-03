#!/usr/bin/env python
import os, stat, errno, fuse
from fuse import Fuse

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class Path:
    def __init__(self):
        self.path=''
    def getattr(self):
        return MyStat()

class File(Path):
    def __init__(self):
        pass

class Dir(Path):
    def __init__(self):
        pass
    def getattr(self):
        #FIXME: Appel à la fonction du parent
        answer =
        answer.st_mode = stat.S_IFDIR | 0755
        anwser.st_nlink = 2

input = Dir()
input.path = '/input'

class RTEFS(Fuse):

    def getattr(self, path):
        st = MyStat()
        if path == '/':
        elif path == input.path:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = len(hello_str)
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        for r in  '.', '..', cwd.path[1:]:
            yield fuse.Direntry(r)

    def open(self, path, flags):
        if path != hello_path:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        if path != hello_path:
            return -errno.ENOENT
        slen = len(hello_str)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = hello_str[offset:offset+size]
        else:
            buf = ''
        return buf

def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
