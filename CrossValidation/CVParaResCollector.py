'''
Created on Mar 31, 2014
collect cv's parameter results
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
import json
from cxBase.WalkDirectory import *
from CrossValidation.FoldNameGenerator import *
import ntpath




class CVParaResCollectorC(cxBaseC):
    
    def SplitFoldParaId(self,EvaName):
        FoldId = 0
        ParaId = 0
        print "to be implemented in sub classes"
        return FoldId,ParaId
    
    
    def LoadEvaMetric(self,EvaName):
        EvaMetric = 0
        print "to be implemented"
        return EvaMetric
    
    def FilterEvaResFName(self,EvaName):
        print 'to be implemented, leave the targets'
        return True
    
    def Init(self):
        self.Namer = FoldNameGeneratorC()
        self.RootDir = ""
        self.K = 5
        self.hFoldBestPara = {} #to collect result, the best para for each fold
        self.Reverse = True #choose the biggest one
        return
    
    
    def SetConf(self,ConfIn):
        self.Namer.SetConf(ConfIn)
        self.RootDir = self.Namer.RootDir
        self.K = self.Namer.K
        conf = cxConf(ConfIn)
        self.Reverse = bool(conf.GetConf('bigfirst'))        
        return True
    
    
    @staticmethod
    def ShowConf():
        FoldNameGeneratorC.ShowConf()
        print "bigfirst 1"
        return True
        
    
    def GetEvaResFName(self):
        lMid = WalkDir(self.Namer.EvaDir())
        lEvaName = []
        for mid in lMid:
            if self.FilterEvaResFName(mid):
                lEvaName.append(mid)            
        return lEvaName
    

    
    
    def Process(self):
        lEvaFName = self.GetEvaResFName()        
        for EvaName in lEvaFName:
            FoldId,ParaId = self.SplitFoldParaId(EvaName)
            EvaMetric = self.LoadEvaMetric(EvaName)
            if not FoldId in self.hFoldBestPara:
                self.hFoldBestPara[FoldId] = [ParaId,EvaMetric]
                continue
            if (self.Reverse & (self.hFoldBestPara[FoldId][1] < EvaMetric)) | ( (not self.Reverse) & (self.hFoldBestPara[FoldId][1] > EvaMetric)):
                self.hFoldBestPara[FoldId] = [ParaId,EvaMetric]
                print "get better para fold[%d] [%d,%s]" %(FoldId,ParaId,str(EvaMetric))
        return dict(self.hFoldBestPara)
    

                
        
        
    
    
