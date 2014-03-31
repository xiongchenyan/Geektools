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
import json,time

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
        Index = 0
        print "start submiting [%s][%d] jobs..." %(JobName, len(lCondor))        
        lJobId = []
        Index = 0
        for i in xrange(0,len(lCondor),100):            
            CondorSubFileName = self.WriteCondorFile(lCondor[i:i+100], JobName,Index)
            Index += 1        
            SubmitOut = subprocess.check_output(['condor_submit',CondorSubFileName])
            lJobId.extend(self.SegJobId(SubmitOut))
            time.sleep(5)                    
        return lJobId
    
    
    def WriteCondorFile(self,lCondor,JobName,Index = 0):
        CondorSubFileName = self.MakeSubFileName(JobName,Index)
        #things in lCondor must be fully made, the JobName and ids
        out = open(CondorSubFileName,'w')
        for Condor in lCondor:
            print >>out, Condor.dumps()
        out.close()                                
        return CondorSubFileName
    
    
    def MakeSubFileName(self,JobName,Index):
        return self.WorkDir + "/Sub" + JobName + "_%d" %(Index)
    
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
    
    
    
    
        