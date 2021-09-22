import os

def isCustomExists():
	return True

def CreatePlainCustom():
	return True

def GenerateUnins(name,isHome):

	if isHome:
		path = "/home/"+name+"/uninstall.sh"
	else:
		path = "/tmp/tmp"

	return True

def GenGrubEntry(name,isHome):
	return True


