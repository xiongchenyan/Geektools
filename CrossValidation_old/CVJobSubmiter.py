'''
Created on Mar 31, 2014
the basic class for cv job submiter.
the general framework is defined here
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
import json
from cxBase.WalkDirectory import *
from CrossValidation_old.FoldNameGenerator import *
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath
from copy import deepcopy
from condor.CondorMulJobSubmiter import CondorMulJobSubmiterC

class CVJobSubmiterC(CondorMulJobSubmiterC):
    def Init(self):
        super(CVJobSubmiterC,self).Init()
    