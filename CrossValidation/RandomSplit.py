'''
Created on Mar 7, 2014
random split
@author: cx
'''

import random,math
import json


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')

from cxBase.base import *
from FoldNameGenerator import *

def DataSplit(lData,K,NeedDev = False):
    llSplit = []
    lChunks = []
    n = int(math.ceil(float(len(lData)/float(K))))
    for i in xrange(0,len(lData),n):
        lChunks.append(lData[i:i+n])
    for i in range(K):
        lTrain = []
        lTest = []
        lDev = []
        for j in range(len(lChunks)):
            if j == i:
                lTest.extend(lChunks[j])
            else:
                if NeedDev & ((j == len(lChunks) - 1) | ((j == len(lChunks) - 2)& (i==len(lChunks) - 1))):
                    lDev.extend(lChunks[j])
                else:             
                    lTrain.extend(lChunks[j])
        llSplit.append([lTrain,lTest,lDev])

#     print "split res:\n%s"%(json.dumps(llSplit,indent=1))
    return llSplit








class DataSpliterC(object):
    #root class for data spliter
    #sub class need to implement LoadData() and OutData() as line->data and data->line
    
    def Init(self):
        self.InName = ""
        self.RootDir = ""
        self.K = 5
        self.NeedDev = True
        self.Random = True
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.NeedDev = bool(int(conf.GetConf('needdev')))
        self.NameCenter = FoldNameGeneratorC(ConfIn)
        self.K = int(conf.GetConf('k', self.K))
        self.Random = bool(int(conf.GetConf('random',1)))
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            DataSpliterC.ShowConf()
            self.SetConf(ConfIn)
        return
    
    @staticmethod
    def ShowConf():
        print "in\nneeddev 1\nrandom 1"
        FoldNameGeneratorC.ShowConf()
        
    
    def LoadData(self):
        #from line to object to store in list
        lData = []
        print "must be implemented in inherited class"
        return lData
    
    def OutData(self,lData,OutName):
        print "must be implemented in inherited class"
        return True 
        
    def Process(self):
        lData = self.LoadData()
        if self.Random:
            random.shuffle(lData)
        llSplit = DataSplit(lData,self.K,self.NeedDev)
        lFileName = self.NameCenter.DataFileName()          
        for i in range(self.K):
            for j in range(len(lFileName[i])):
                self.OutData(llSplit[i][j],lFileName[i][j])
                
        return True
    
    
        
        
        
    
    
    
        
    
        
    
        
    
    
        

