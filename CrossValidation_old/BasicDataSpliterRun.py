'''
Created on Apr 8, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from RandomSplit import *
from FoldNameGenerator import *
class BasicDataSpliterC(DataSpliterC):
    
    def LoadData(self):
        lData = [line.strip() for line in open(self.InName)]
        return lData
    
    def OutData(self,lData,OutName):
        out = open(OutName,'w')
        for line in lData:
            print >>out, line
        out.close()
        return True
    
    



def BasicDataSpliterUnitRun(ConfIn):
    BasicDataSpliterC.ShowConf()
    Spliter = BasicDataSpliterC(ConfIn)
    Spliter.Process()
    return True


import sys    
     
if 2 != len(sys.argv):
    print "1conf:"
    BasicDataSpliterC.ShowConf()
    sys.exit()
    
BasicDataSpliterUnitRun(sys.argv[1])