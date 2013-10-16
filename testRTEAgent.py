#!/usr/bin/env python3

#This test checks that the RTEAgent can use the ramdisk and actually compile and view the examples it is given.
#This test do not use the Fuse filesystem, nor do we need a text editor
from RTEAgent import *
logging.getLogger().setLevel(logging.DEBUG)


f = open( "main1.tex",'r')
main1 = f.read()
f.close()
f = open( "main2.tex",'r')
main2 = f.read()
f.close()
f = open( "main3.tex",'r')
main3 = f.read()
f.close()
agent = RTEAgent()
var = input("Enter something: ")
print("Testing to put main1.tex contents in main")
agent.input("main.tex",main1)
var = input("Enter something: ")
print("main 2....")
agent.input("main.tex",main2)
var = input("Enter something: ")
print("main 3...")
agent.input("main.tex",main3)
