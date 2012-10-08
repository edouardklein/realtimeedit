#!/usr/bin/env python
import os, stat, errno, fuse
from fuse import Fuse
fuse.fuse_python_api = (0, 2)

def Llog( aString ):
    f = open("/tmp/FuseDB.log","a")
    f.write( aString )
    f.close()

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
    def __init__(self, path=''):
        self.path=path
    def getattr(self):
        return MyStat()

class File(Path):
    buffer = ''
    def getattr(self):
        answer = Path.getattr( self )
        answer.st_mode = stat.S_IFREG | 0777
        answer.st_nlink = 1
        answer.st_size = len(self.buffer)
        Llog( "gettattr de File\n") 
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
        answer = Path.getattr( self )
        answer.st_mode = stat.S_IFDIR | 0777
        answer.st_nlink = 2
        return answer

Dot = Dir('.')
DotDot = Dir('..')
Root = Dir('/')
Input = Dir('/input')
Error = File('/error.txt')
Error.buffer = "Coucou"
   
class RTEFS(Fuse):

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
        return matchingEl[0]
    
    def getattr(self, path):
        Llog( "getattr1 sur "+path+", we try\n")
        file = None
        try:
            file = self.matchByPath( path )
        except IOError:
            if Input in self.FS and path[0:7] == '/input/':
                Llog( "\tGetAttr sur un fichier d'input\n")
                return File(path).getattr()
            Llog( "\treturn error"+"\n")
            f.close()
            return -errno.ENOENT
        Llog( "\treturn un truc"+str(file)+"\n")
        return file.getattr()
    
    def readdir(self, path, offset):
        Llog( "readdir sur "+path+"\n")
        for r in  [f for f in self.FS if f.path != '/']:
            path = r.path
            if path[0] == '/':
                path=path[1:]
            Llog( "\treaddir sur "+path+"\n")
            yield fuse.Direntry(path)

    def chmod ( self, path, mode ):
        Llog( "chmod sur "+path+"\n")
        return 0
    
    def chown ( self, path, uid, gid ):
        Llog( "chown sur "+path+"\n")
        return 0
    
    def utime ( self, path, times ):
        Llog( "utime sur "+path+"\n")
        return 0
       
    def mknod(path, mode, rdev):
        Llog( "mknod sur "+path+"\n")
        return 0

    def create(path, mode, rdev):
        Llog( "mknod sur "+path+"\n")
        return 0
       


            
    def open(self, path, flags):
        Llog( "open sur "+path+"\n")
        file = None
        try:
            file = self.matchByPath( path )
        except IOError:
            if Input in self.FS and path[0:7] == '/input/':
                Llog( "Open sur un fichier d'input\n")
                return
            else:
                return -errno.ENOENT

    def read(self, path, size, offset):
        Llog( "read sur "+path+"\n")
        try:
            file = self.matchByPath( path )
        except IOError:
            return -errno.ENOENT
        return file.read( size, offset )
    def write ( self, path, buf, offset ):
        LLog("Write sur "+path+"\n")
        return len(buf)
def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    Llog( "toto"+"\n")
    
    server = RTEFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
