'''
Created on Mar 25, 2014

@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import *
import os

class FoldNameGeneratorC:
    def Init(self):
        self.RootDir = ""
        self.K = 5
        self.DataSuffix = "data/"
        self.ParaSuffix = "para/"
        self.EvaSuffix = 'eva/'
        self.ConfSuffix = 'conf/'
        self.SubSuffix = 'sub/'   
        self.PredictSuffix = 'pred/'     
        self.OutSuffix = 'out/'
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.RootDir = conf.GetConf('rootdir')
        self.K = int(conf.GetConf('k'))
        self.CreateDir()
        return True
    
    
    def __init__(self,ConfIn=''):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    
    
    @staticmethod
    def ShowConf():
        print"rootdir\nk 5"
    
    
    @staticmethod
    def SplitFoldId(name):
        vCol = name.split('_')
        if len(vCol) < 2:
            return '0'
        return int(vCol[len(vCol)-1])
    
    def DataDir(self):
        return self.RootDir + '/' + self.DataSuffix
    def ParaDir(self):
        return self.RootDir + '/' + self.ParaSuffix
    def EvaDir(self):
        return self.RootDir + '/' + self.EvaSuffix
    def ConfDir(self):
        return self.RootDir + '/' + self.ConfSuffix
    def SubDir(self):
        return self.RootDir + '/' + self.SubSuffix
    
    def OutDir(self):
        return self.RootDir + '/' + self.OutSuffix
    
    def PredictDir(self):
        return self.RootDir + "/" + self.PredictSuffix
    
    def AllSubDir(self):
        return [self.DataDir(),self.ParaDir(),self.EvaDir(),self.ConfDir(),self.SubDir(),self.PredictDir()]
    
    def CreateDir(self):
        for DirName in self.AllSubDir():
            if not os.path.exists(DirName):
                os.makedirs(DirName)
        return
    
    
    def DataFileName(self):
        #return a [trainname,testname,devname] list, len = K
        lRes = []
        for i in range(self.K):
            lRes.append([self.DataDir()+'/train_%d'%(i),self.DataDir()+'/test_%d'%(i),self.DataDir()+'/dev_%d'%(i)])
        return lRes
    
    
                
            
        