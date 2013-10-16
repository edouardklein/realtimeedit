#!/usr/bin/env python
import os
import logging
import subprocess

mount_tmpfs_command = r'diskutil erasevolume HFS+ "ramdisk" `hdiutil attach -nomount ram://1165430`' # from http://osxdaily.com/2007/03/23/create-a-ram-disk-in-mac-os-x/
umount_tmpfs_command = r'umount /Volumes/ramdisk && hdiutil detach /dev/disk1' #make disk1 a variable, it is not always disk1
#mount_tmpfs_command = "/home/edouard/Documents/relatimeedit/linux/mount_tmpfs.sh"
#umount_tmpfs_command = "//home/edouard/Documents/relatimeedit/linux/umount_tmpfs.sh"

class RTEAgent:

    def __init__( self, cwd=os.getcwd(), compileCmd="make RTEcompile", firstViewCmd="make RTEstartView", viewCmd="make RTEview", stopViewCmd="make RTEstopView", ramdisk="/Volumes/ramdisk" ):
        self.cwd = cwd
        self.compileCmd = compileCmd
        self.ramdisk = ramdisk
        self.firstViewCmd = firstViewCmd
        self.viewCmd = viewCmd
        self.stopViewCmd = stopViewCmd
        self.cdToRamdiskCmd = "cd "+self.ramdisk+" && "
        logging.debug("Mounting the ramdisk")
        self.mountRamDisk()
        logging.debug("Copying to ramdisk")
        self.cpyWDtoRamdisk()
        logging.debug("First compilation and view")
        logging.debug( "Running : "+self.cdToRamdiskCmd+self.compileCmd+"&&"+self.firstViewCmd)
        subprocess.Popen(self.cdToRamdiskCmd+self.compileCmd+" && "+self.firstViewCmd, shell=True )
        logging.debug("Done")

    def __del__(self):
        self.umountRamDisk()
        
    def input( self, filename, contents ):
        logging.debug("Input recieved, compiling")
        logging.debug("contents :"+contents)
        f = open( self.ramdisk+'/'+filename, "w" )
        f.write(  contents )
        f.close()
        try:
            logging.debug( "Running : "+self.cdToRamdiskCmd+self.compileCmd)
            subprocess.check_output( self.cdToRamdiskCmd+self.compileCmd, shell=True )
            logging.debug( "done")
        except subprocess.CalledProcessError as err:
            return err.returncode, err.output
        logging.debug( "Running : "+self.cdToRamdiskCmd+self.viewCmd)
        subprocess.check_output( self.cdToRamdiskCmd+self.viewCmd, shell=True ) #Voluntarily uncaught exception, there should be no error there
        logging.debug("done")
        self.state="Waiting"
        return 0

    def mountRamDisk(self):
        #FIXME: gracefully handling permissions would be nice
        #FIXME: A way to change the size of the ramdisk would be nice
        logging.debug("Ramdisk command : "+mount_tmpfs_command)
        subprocess.check_call(mount_tmpfs_command,shell=True)

    def umountRamDisk(self):
        #FIXME: gracefully handling permissions would be nice
        #FIXME: A way to change the size of the ramdisk would be nice
        subprocess.check_call(self.stopViewCmd+"&& sleep 1",shell=True)
        subprocess.check_call(umount_tmpfs_command+" "+self.ramdisk ,shell=True)

    def cpyWDtoRamdisk( self ):
        subprocess.check_call("cp -r "+self.cwd+"/* "+self.ramdisk+"/", shell=True)
        
        
