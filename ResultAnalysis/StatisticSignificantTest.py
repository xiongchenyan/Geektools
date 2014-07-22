'''
Created on Jun 26, 2014
test the statistic signification of Ad hoc results
input: lName, lPerQMeasure[[one q measure],[another methods]], lBaselineName
do: compare all lName to lBaseLineName, if Avg> and significant
output: lSignificantMtx[len(lName) * len(lBaseLineName)], 0:not, real value: yes and output p
@author: chenyan
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from AdhocEva.AdhocMeasure import *
import math,random

class StatisticSignificantTestC(cxBaseC):
    
    def Init(self):
#         self.MaxP = 0.05
        self.lName = []
        self.lResInName = []
        self.lBaseName = []
        self.lPerQMeasure = []
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
#         self.MaxP = float(conf.GetConf('maxp',self.MaxP))
        self.lName = conf.GetConf('methodname',[])
        self.lBaseName = conf.GetConf('baseline',[])
        self.lResInName = conf.GetConf('methodevares',[])
        
    @staticmethod
    def ShowConf():
        print 'methodname\nbaseline\nmethodevares'
        
    def ReadEvaRes(self):
        del self.lPerQMeasure[:]
        for InName in self.lResInName:
            lPerQ = AdhocMeasureC.ReadPerQEva(InName,False)
            lPerQ.sort(key = lambda item: item[0])
            self.lPerQMeasure.append(lPerQ)
            
        for i in range(1,len(self.lPerQMeasure)):
            self.lPerQMeasure[i] = AdhocMeasureC.FillMissEvaByBaseline(self.lPerQMeasure[i], self.lPerQMeasure[0])
        return True
    
    
    def Process(self,lName = [],lBaseName = [],lPerQMeasure = []):
        '''
        lPerQMeasure must not have missing values, and must sortted by qid
        prefer to use conf and read myself, everything is ready then
        return a method * base line method result matrix, each element a Measure, showing the p value
        '''
        if [] == lName: 
            self.ReadEvaRes()
            lName = self.lName
            lBaseName = self.lBaseName
            lPerQMeasure = self.lPerQMeasure
            
        lResMtx = []
        
        for i in range(len(lPerQMeasure)):
            lThisMethodRes = []
            for j in range(len(lBaseName)):
                
                if not lBaseName[j] in lName:
                    lThisMethodRes.append(AdhocMeasureC())
                    continue
                p = lName.index(lBaseName[j])
                lMeasure = lPerQMeasure[i]
                lBaseMeasure = lPerQMeasure[p]
                print "testing [%s] vs [%s]" %(lName[i],lBaseName[j])
                Measure  = self.StaticTest(lMeasure,lBaseMeasure)
                print "res [%s]" %(Measure.dumps())
                lThisMethodRes.append(Measure)
            lResMtx.append(lThisMethodRes)
            
#         for i in range(len(lResMtx)):
#             for j in range(len(lResMtx[i])):
#                 for name in AdhocMeasureC.MeasureName():
#                     if lResMtx[i][j].GetMeasure(name) >= self.MaxP:
#                         lResMtx[i][j].SetMeasure(name,0)
        return lName, lResMtx
    
    
    
    
    def StaticTest(self,lMeasure,lBaseMeasure):
        '''
        check whether the measures are significant better
        for map,ndcg,err
        lMeasure now is [qid,MeasureC]
        '''
        Measure = AdhocMeasureC()
        
        lMeasure.sort(key = lambda item: item[0])
        lBaseMeasure.sort(key = lambda item: item[0])
        
        lPureMeasure = [item[1] for item in lMeasure]
        lPureBase = [item[1] for item in lBaseMeasure]
        
        for name in AdhocMeasureC.MeasureName():
            lTarget = [item.GetMeasure(name) for item in lPureMeasure]
            lBase = [item.GetMeasure(name) for item in lPureBase]
            
            '''    
            check if target is better than base, if not, then set p value to 1 and do not do test
            '''
            if (len(lTarget) == 0) | (len(lBase) == 0):
                Measure.SetMeasure(name,1)
                continue
            if (sum(lTarget) / float(len(lTarget))) <= (sum(lBase) / float(len(lBase))):
                Measure.SetMeasure(name,1)
                continue
            Measure.SetMeasure(name, self.CalcPValue(lTarget,lBase))
            
        return Measure
    
    
    
    def CalcPValue(self,lTarget,lBase):
        '''
        the very end of significant test
        left for sub class
        '''
        
        print "please call subclass for CalcPValue's implementation"
        return 0
    
    
    
class FisherRandomizationTestC(StatisticSignificantTestC):
    
    def CalcPValue(self,lTarget,lBase):
        TotalTest = 2000
        Diff = sum(lTarget) / float(len(lTarget)) - sum(lBase) / float(len(lBase))
        cnt = 0.0
        for i in range(TotalTest):
            lA,lB = self.RandomExchange(lTarget, lBase)
            ThisDiff = sum(lA) / float(len(lA)) - sum(lB) / float(len(lB))
            if ThisDiff > Diff:
                cnt += 1.0
        p = cnt / float(TotalTest)
        return p
        
        
    def RandomExchange(self,lTarget,lBase):
        lA = list(lTarget)
        lB = list(lBase)
        
        for i in range(len(lTarget)):
            if random.randint(0,1):
                lA[i],lB[i] = lB[i],lA[i]
        return lA,lB    
        
        
