'''
Created on Mar 25, 2014
submit jobs to condor
input: list of CondorC
    working dir
    job name
    (submit jobname+job id as position in lSub)
submit to condor
output: list of job id?
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')


import subprocess
from CondorBase import *
import json

class CondorSubmiterC(object):
    def Init(self):
        self.WorkDir = ""
        
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" == ConfIn:
            self.SetConf(ConfIn)
        
            
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.WorkDir = conf.GetConf('workdir')
        return True
        
    @staticmethod
    def ShowConf():
        print "workdir"
    
    def Submit(self,lCondor,JobName):
        
        CondorSubFileName = self.WriteCondorFile(lCondor, JobName)
        print "start submiting [%s][%d] jobs..." %(JobName, len(lCondor))
        SubmitOut = subprocess.check_output(['condor_submit',CondorSubFileName])
        lJobId = self.SegJobId(SubmitOut)        
        return lJobId
    
    
    def WriteCondorFile(self,lCondor,JobName):
        CondorSubFileName = self.MakeSubFileName(JobName)
        #things in lCondor must be fully made, the JobName and ids
        out = open(CondorSubFileName,'w')
        for Condor in lCondor:
            print >>out, Condor.dumps()
        out.close()                                
        return CondorSubFileName
    
    
    def MakeSubFileName(self,JobName):
        return self.WorkDir + "/Sub" + JobName
    
    def SegJobId(self,OutPut):
        lJobId = []
        print "TBD"
        lLine = OutPut.split('\n')
        for line in lLine:            
            if 'submitted to cluster' in line:
                vCol = line.strip('.').split()                
                JobId = vCol[len(vCol) - 1]
                lJobId.append(JobId)                     
        return lJobId
    
    
def CondorSubmitUnitTest(ConfIn):
    CondorSubmiterC.ShowConf()
    print "jobname test\ncondorin"
    conf = cxConf(ConfIn)
    CondorSubmiter = CondorSubmiterC(ConfIn)
    Condor = cxCondorC(conf.GetConf('condorin'))    
    JobName = conf.GetConf('jobname')    
    
    lJob = CondorSubmiter.Submit([Condor], JobName)
    print 'submit jobs:\n%s' %(json.dumps(lJob))
    return True
    
    
    
    
        