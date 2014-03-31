'''
Created on Mar 31, 2014
the basic class for cv job submiter.
the general framework is defined here
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
import json
from cxBase.WalkDirectory import *
from CrossValidation.FoldNameGenerator import *
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath
from copy import deepcopy


class CVJobSubmiterC(object):
    
    
    def Init(self):
        self.RootDir = ""
        self.K = 5
        self.Namer = FoldNameGeneratorC()
        self.CondorBase = cxCondorC()
        self.ConfBase = cxConf()
        self.JobName = "CV"
        
        
    def SetConf(self,ConfIn):
        self.Namer.SetConf(ConfIn)
        self.RootDir = self.Namer.RootDir
        self.K = self.Namer.K
        conf = cxConf(ConfIn)
        self.CondorBase.LoadSub(conf.GetConf('condorbase'))
        self.ConfBase.LoadConf(conf.GetConf('confbase'))
        self.JobName = conf.GetConf('jobname')
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
    @staticmethod
    def ShowConf():
        FoldNameGeneratorC.ShowConf()
        print "condorbase\nconfbase\njobname"
        
    
    
    def InitCollectRes(self):
        #sub class will collect and set data sources here
        print "root class, nothing to collect"
        return True
        
    
    def LoadFName(self):
        lFName = self.Namer.DataFileName()
        return lFName
    
    def LoadParaName(self):
        lParaName = WalkDir(self.Namer.ParaDir()) #para index is exactly the para fname
        return lParaName
    
    
    def FNameParaPairValid(self,FName,ParaName):
        #check whether this paraset appliable to this FName
        #if not return False
        #using information set in InitCollectRes
        return True
    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        conf = deepcopy(self.ConfBase)
        return conf
    
    
    def GenerateSubForConf(self,conf,ConfIndex):
        condor = deepcopy(self.CondorBase)        
        ConfFName = self.Namer.ConfDir() + "_%d" %(ConfIndex)
        conf.dump(ConfFName)
        oldargu = list(condor.GetCondor('arguments'))
        oldargu[len(oldargu) - 1] = ConfFName
        
        condor.SetCondor('arguments',oldargu)
        condor.SetCondor('output',condor.GetCondor('output') + self.JobName + "_%d"%(ConfIndex))
        condor.SetCondor('error',condor.GetCondor('error') + self.JobName + "_%d"%(ConfIndex))
        condor.SetCondor('log',condor.GetCondor('log') + self.JobName + "_%d"%(ConfIndex))
        return condor
    
    
    def Process(self):
        self.InitCollectRes()      
        
        lFName = self.LoadFName()
        lParaName = self.LoadParaName()
        
        lSub = []
        ConfIndex = 0
        print "start to make sub file for [%d] data partition [%d] para" %(len(lFName),len(lParaName))
        for FName in lFName:
            for ParaName in lParaName:
                if not self.FNameParaPairValid(FName, ParaName):
                    continue
                conf = self.GenerateConfForPair(FName, ParaName)
                sub = self.GenerateSubForConf(conf, ConfIndex)
                ConfIndex += 1
                lSub.append(sub)
                
        CondorSubmiter = CondorSubmiterC()
        CondorSubmiter.WorkDir = self.Namer.SubDir()
        lJobId = CondorSubmiter.Submit(lSub, self.JobName)        
        print "submitted job ids:\n%s" %(json.dumps(lJobId))        
        return lJobId
        
        
        

    
    
    
    
    
    
    