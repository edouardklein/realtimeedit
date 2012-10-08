#!/usr/bin/env python
import os, stat, errno, fuse
f = open("/tmp/mnt/input/tesfdfdfdfdt","w")
print "F vaut" + str(f)
f.write("testr")
print "F vaut" + str(f)
f.close()

