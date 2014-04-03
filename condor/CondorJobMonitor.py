'''
Created on Apr 1, 2014

@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')

from cxBase.base import *

import subprocess
import json
import time


class CondorJobMonitorC(cxBaseC):
    def Init(self):
        self.User = 'cx'
        self.CheckFreq = 600 #600s a condor_q
        self.VarifyLog = False #whether
        self.LogDir = "/bos/user0/cx/tmp/log/" #log file path
        self.MaxCheckNum = 120
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.VarifyLog = bool(int(conf.GetConf('varifylog',0)))
        self.LogDir = conf.GetConf('logdir', self.LogDir)
        self.CheckFreq = conf.GetConf('checkfreq', self.CheckFreq)
        self.User = conf.GetConf('user', self.User)
        return True
    
    @staticmethod
    def ShowConf():
        print "logdir\nvarifylog\ncheckfreq\nuser"
        return
    
    
    def Monitor(self,lTargetJob=[],JobName=""):
        #wait until all lJob finishe in condor q
        CheckNum = 0
        
        while CheckNum < self.MaxCheckNum:
            OutStr = subprocess.check_output(['condor_q','user %s' %(self.User)])
            lJob = self.SplitCondorJobId(OutStr)
            JobFinished = True
            RunningJobCnt = 0
            if (lTargetJob == []):
                #no specific job, all user's job must finished
                RunningJobCnt = len(lJob)
            else:
                for Job in lTargetJob:
                    if Job in lJob:
                        RunningJobCnt += 1
            if RunningJobCnt > 0:
                JobFinished = False
            
            if JobFinished:
                if self.VarifyLog:
                    if not self.CheckLogStatus(JobName):
                        print "job group [%s] has failed jobs" %(JobName)
                        return False
                    return True
                else:
                    return True
            print "[%d] check, running job [%d]" %(CheckNum,RunningJobCnt)
            print "waiting for [%d] sec" %(self.CheckFreq)
            time.sleep(self.CheckFreq)
            CheckNum += 1        
        print "time out"
        return False
    
    
    def SplitCondorJobId(self,OutStr):
        lJob = []
        for line in OutStr.split('\n'):
            print "spliting line [%s]"
            vCol = line.split()
            if len(vCol) > 2:
                if self.User == vCol[1]:
                    lJob.append(vCol[0].split('.')[0])
        print "user's running jobs\n%s" %(json.dumps(lJob))
        return lJob
    
    def CheckLogStatus(self,JobName):
        print "not implemented"
        return True