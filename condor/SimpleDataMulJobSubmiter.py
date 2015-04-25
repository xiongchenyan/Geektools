'''
Created on Apr 23, 2014
simple job submiter
update the conf in and out
in: test_%d in data
out: out/%d in out()
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
from cxBase.WalkDirectory import *
from CrossValidation_old.FoldNameGenerator import *
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath
from copy import deepcopy
from condor.CondorMulJobSubmiter import CondorMulJobSubmiterC


class SimpleDataMulJobSubmiterC(CondorMulJobSubmiterC):
    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        conf = deepcopy(self.ConfBase)
        conf.SetConf('in',FName[1])
        FoldIndex = FoldNameGeneratorC().SplitFoldId(FName[1])
        conf.SetConf('out',self.Namer.OutDir() + "/%d" %(FoldIndex))
        
        return conf
    



import sys

if 2 != len(sys.argv):
    print "1 conf"
    SimpleDataMulJobSubmiterC.ShowConf()
    sys.exit()
    
    
Submiter = SimpleDataMulJobSubmiterC(sys.argv[1])

Submiter.Process()

print "finished"