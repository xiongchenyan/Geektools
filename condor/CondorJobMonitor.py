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
        
        
    def SetConf(self,ConfIn):
        
        return True
    
    @staticmethod
    def ShowConf():
        
        return
    
    
    def Process(self,lTargetJob,JobName=""):
        #wait until all lJob finishe in condor q
        
        return True
    
    
    def SplitCondorJobId(self,OutStr):
        lJob = []
        return lJob