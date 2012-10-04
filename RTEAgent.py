#!/usr/bin/env python
import os


class RTEAgent:

    def __init__( self, cwd=os.getcwd(), compileCmd="make", viewCmd="make view", ramdisk="/tmp/mnt1" ):
        self.cwd = cwd
        self.compileCmd = compileCmd
        self.viewCmd = viewCmd
        self.ramdisk = ramdisk
        self.mountRamDisk()
        self.cpyWDtoRamdisk()

    def __del__(self):
        self.umountRamDisk()
        
    def input( self, filename, contents ):
        f = open( filename, "w" )
        sys.write( f, contents )
        f.close()
        try:
            subprocess.check_output( self.compileCmd )
        except subprocess.CalledProcessError as err:
            return err.returncode, err.output
        subprocess.check_output( self.viewCmd ) #Voluntarily uncaught exception, there should be no error there
        self.state="Waiting"
        return 0

    def mountRamDisk(self):
        #FIXME: gracefully handling permissions would be nice
        #FIXME: A way to change the size of the ramdisk would be nice
        subprocess.check_call("mount -t tmpfs -o size=256M tmpfs "+self.ramdisk )

    def cpyWDtoRamdisk( self ):
        subprocess.check_call("cp -r "+self.cwd+"/ "+self.ramdisk+"/" )
        
        
