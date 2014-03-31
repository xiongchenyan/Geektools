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




