#!/usr/bin/env python
import os
import logging
import subprocess

mount_tmpfs_command = "/Users/edouard/Projets/relatimeedit/mount_tmpfs.sh"
umount_tmpfs_command = "/Users/edouard/Projets/relatimeedit/umount_tmpfs.sh"

class RTEAgent:

    def __init__( self, cwd=os.getcwd(), compileCmd="make RTEcompile", viewCmd="make RTEview", ramdisk="/tmp/mnt1" ):
        self.cwd = cwd
        self.compileCmd = compileCmd
        self.viewCmd = viewCmd
        self.ramdisk = ramdisk
        logging.debug("Mounting the ramdisk")
        self.mountRamDisk()
        logging.debug("Copying to ramdisk")
        self.cpyWDtoRamdisk()
        logging.debug("Done")

    def __del__(self):
        self.umountRamDisk()
        
    def input( self, filename, contents ):
        logging.debug("Input recieved, compiling")
        f = open( filename, "w" )
        f.write(  contents )
        f.close()
        try:
            subprocess.check_output( self.compileCmd, shell=True )
        except subprocess.CalledProcessError as err:
            return err.returncode, err.output
        subprocess.check_output( self.viewCmd, shell=True ) #Voluntarily uncaught exception, there should be no error there
        self.state="Waiting"
        return 0

    def mountRamDisk(self):
        #FIXME: gracefully handling permissions would be nice
        #FIXME: A way to change the size of the ramdisk would be nice
        logging.debug("Ramdisk command : "+mount_tmpfs_command+" "+self.ramdisk)
        subprocess.check_call(mount_tmpfs_command+" "+self.ramdisk ,shell=True)

    def umountRamDisk(self):
        #FIXME: gracefully handling permissions would be nice
        #FIXME: A way to change the size of the ramdisk would be nice
        subprocess.check_call(umount_tmpfs_command+" "+self.ramdisk ,shell=True)

    def cpyWDtoRamdisk( self ):
        subprocess.check_call("cp -r "+self.cwd+"/ "+self.ramdisk+"/", shell=True)
        
        
