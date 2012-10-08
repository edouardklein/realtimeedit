#====/usr/bin/env python====

#
# CupsFS.py: a FUSE filesystem for mounting an LDAP directory in Python
# Need python-fuse bindings, and an LDAP server.
# usage: ./CupsFS.py <mountpoint>
# unmount with fusermount -u <mountpoint>
#

import stat
import errno
import fuse
from time import time

fuse.fuse_python_api = (0, 2)

def Llog( aString ):
    f = open("/tmp/FuseDB.log","a")
    f.write( aString )
    f.close()


class DirStat(fuse.Stat):
    def __init__(self):
        self.st_mode = stat.S_IFDIR | 0777
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 2
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class FileStat(fuse.Stat):
    def __init__(self):
        self.st_mode = stat.S_IFREG | 0777
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 1
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = -1
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class Path:
    def __init__(self, path=''):
        self.path=path

class File(Path):
    buffer = ''
    def getattr(self):
        answer = FileStat()
        answer.st_size = len(self.buffer)
        return answer
    def read( self, size, offset ):
        slen = len(self.buffer)
        Llog( "\tread de File"+str(offset)+"sz"+str(size)+"\n") 
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = self.buffer[offset:offset+size]
        else:
            buf = ''
        #Llog( "\tread de File"+buf+"\n") 
        return buf

class Dir(Path):
    def getattr(self):
        return DirStat()



Dot = Dir('.')
DotDot = Dir('..')
Root = Dir('/')
Input = Dir('/input')
Error = File('/error.txt')
Error.buffer = "Coucou\n"

class RTEFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)

    FS = [Dot,DotDot,Root,Error,Input]
    State = "Waiting"    
        
    def matchByPath( self, path ):
        #Llog( "matchbypath sur "+path+"\n")
        matchingEl = [ x for x in self.FS if x.path==path]
        #Llog( "matching el a une valeur"+str(len(matchingEl))+"\n")
        
        if len(matchingEl) == 0:
            #Llog( "\tmatchbypath raises an error\n")
            raise IOError()
        assert( len(matchingEl) == 1)
        Llog( "\tmatchbypath returns something\n")
        return matchingEl[0]        # Get our list of printers available.
                
    def getattr(self, path):
        Llog( "getattr1 sur "+path+", we try\n")
        file = None
        answer = None
        if Input in self.FS and path[0:7] == '/input/':
            Llog( "\tGetAttr sur un fichier d'input\n")
            answer = File(path).getattr()
        else:
            try:
                file = self.matchByPath( path )
            except IOError:
                Llog( "\treturn error"+"\n")
                f.close()
                return -errno.ENOENT
            answer =  file.getattr()
        answer.st_atime = int(time())
        answer.st_mtime = answer.st_atime
        answer.st_ctime = answer.st_atime
        Llog( "\treturn un truc"+str(answer)+"\n")
        return answer
                
        def readdir(self, path, offset):
            Llog( "readdir sur "+path+"\n")
            for r in  [f for f in self.FS if f.path != '/']:
                path = r.path
                if path[0] == '/':
                    path=path[1:]
                    Llog( "\treaddir sur "+path+"\n")
                    yield fuse.Direntry(path)
 
        def mknod(path, mode, rdev):
            Llog( "mknod sur "+path+"\n")
            return 0

        def unlink(self, path):
            Llog( "unlink sur "+path+"\n")
            return 0

        def read(self, path, size, offset):
            Llog( "read sur "+path+"\n")
            try:
                file = self.matchByPath( path )
            except IOError:
                return -errno.ENOENT
            return file.read( size, offset )

        def write(self, path, buf, offset): 
            LLog("Write sur "+path+"\n")
            return len(buf)
                            
        def release(self, path, flags):
            LLog("release sur "+path+"\n")
            return 0

        def utimens(self, path, garbage1, garbage2):
            LLog("utimens sur "+path+"\n")
            return 0
           
                                
        def open(self, path, flags):
            return 0
        
        def truncate(self, path, size):
            return 0
        
        def utime(self, path, times):
            return 0
        
        def mkdir(self, path, mode):
            return 0
        
        def rmdir(self, path):
            return 0
        
        def rename(self, pathfrom, pathto):
            return 0
        
        def fsync(self, path, isfsyncfile):
            return 0
        
def main():
    usage="""
      rte fs
      """ + fuse.Fuse.fusage
                                    
    server = RTEFS(version="%prog " + fuse.__version__,
                   usage=usage, dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()
    
if __name__ == '__main__':
    main()


                                        
