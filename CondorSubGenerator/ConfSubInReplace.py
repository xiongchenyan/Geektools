'''
Created on Apr 2, 2013
replace the in or arguments of a conf/sub file
in:conf/sub + inname + sub|conf + outname

make sure the conf and sub's in/arguments(log,output,error) already put with directory name
@author: cx
'''





def LoadConf(sIn):
        hConf={}
        for line in open(sIn):
            vCol = line.strip().split(' ')
            if (len(vCol) < 2):
                continue
            hConf[vCol[0]] = " ".join(vCol[1:len(vCol)])
        return hConf
def LoadSub(sIn):
    hSub={}
    for line in open(sIn):
        vCol = line.strip().split('=')
        if (len(vCol) < 2):
            continue
        hSub[vCol[0].lower()] = vCol[1]
    return hSub


def ReplaceInOut(hDict,name):
    if ("in" in hDict):
        hDict["in"] += name
    if ("out" in hDict):
        hDict["out"] += name + "_res"
    if ("arguments" in hDict):
        hDict["arguments"] += name
    if ("log" in hDict):
        hDict["log"] += name + "_log"
    if ("output" in hDict):
        hDict["output"] += name + "_out"
    if ("error" in hDict):
        hDict["error"] += name + "_err"
    return True

def Out(hDict,InType,OutName):
    spliter = " "
    if (InType == "sub"):
        spliter = "="
    out = open(OutName,"w")
    for item in hDict:
        print >> out,item + spliter + hDict[item]
    if (InType == "sub"):
        print >> out,"queue"
    out.close()
    return True  


import sys

if (5 != len(sys.argv)):
    print "4 argu:conf/sub + inname + sub|conf + outname "
    print "make sure the conf and sub's in/arguments(log,output,error) already put with directory name"
    sys.exit()

InType = sys.argv[3]
name = sys.argv[2]
sIn=sys.argv[1]
sOut=sys.argv[4]

hDict = {}
print "start on [%s][%s][%s][%s]" %(sIn,name,InType,sOut)
if (InType == "sub"):
    hDict = LoadSub(sIn)
else:
    hDict = LoadConf(sIn)
print "read done"
ReplaceInOut(hDict,name)
print "replace done"
Out(hDict,InType,sOut)
print "done"    
        
        