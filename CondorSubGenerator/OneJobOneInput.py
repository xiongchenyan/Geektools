'''
Created on Feb 11, 2014
input: a conf file, a sub file
output:one conf file for each input, one sub contain all jobs
conf file's in and out only refers to input and output directory
traverse all sub files in input dir, for each file, make a job 
@author: cx
'''



import site
site.addsitedir('/bos/usr4/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr4/cx/cxPylib')
import copy
from cxBase.WalkDirectory import *


def ReadConf(InName):
    hConf = {}
    for line in open(InName):
        vCol = line.strip().split(' ')
        hConf[vCol[0]] = vCol[1]
    return hConf

def ReadSub(InName):
    hSub = {}
    for line in open(InName):
        vCol = line.strip().split('=')
        if len(vCol) < 2:
            continue
        hSub[vCol[0].lower()]=vCol[1]
    return hSub

def OutConf(hConf):
    res = ""
    for item in hConf:
        res += item + " " + hConf[item] + '\n'
    return res.strip()

def OutSub(hSub):
    res = ""
    for item in hSub:
        res += item + "=" + hSub[item] + '\n'
    return res.strip()

def MultipleByInName(hConf,hSub,lInName):
    #lInName is suffix after in dir
    lhConf = []
    lhSub = []
    for InName in lInName:
        hMidConf = copy.deepcopy(hConf)
        hMidSub = copy.deepcopy(hSub)
        hMidConf['in'] += InName
        hMidConf['out'] += InName
        hMidSub['arguments'] += "_" + InName
        hMidSub['log'] += "_" + InName
        hMidSub['error'] += "_" + InName
        hMidSub['output'] += "_" + InName
        lhConf.append(hMidConf)
        lhSub.append(hMidSub)
        
    return lhConf,lhSub


def MakeInName(InDir):
    lFName = WalkDir(InDir)
    for i in range(len(lFName)):
        print lFName[i]
        lFName[i] = lFName[i].replace(InDir,'')
        while lFName[i][0] == '/':
            lFName[i] = lFName[i][1:len(lFName)]
    return lFName

def OutConfSub(lhConf,lhSub,lInName,ConfInName,SubInName):
    SubOut = open(SubInName + "MulIn",'w')
    for i in range(len(lInName)):
        out = open(ConfInName+"_" + lInName[i],'w')
        print >> out, OutConf(lhConf[i])
        out.close()
        print >> SubOut, OutSub(lhSub[i])
        print >> SubOut, "queue"
    SubOut.close()
        
        
        
import sys
import json
if 3 != len(sys.argv):
    print "conf in + sub in\nconf in:indir, out:outdir, sub's arguments is conf, log etc is dir"
    sys.exit()
    
hConf = ReadConf(sys.argv[1])
print "read conf\n" + json.dumps(hConf)
hSub = ReadSub(sys.argv[2])
print "read sub\n" + json.dumps(hSub)
lInName = MakeInName(hConf['in'])
print "get in names\n" + json.dumps(lInName)
lhConf,lhSub = MultipleByInName(hConf,hSub,lInName)
OutConfSub(lhConf,lhSub,lInName,sys.argv[1],sys.argv[2])

print "done" 
        
         
