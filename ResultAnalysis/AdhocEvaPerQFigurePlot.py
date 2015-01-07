'''
Created on Apr 3, 2014
plot per q vs baseline figures
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxConf
from ResultAnalysis.AdhocResAnalysis import AdhocResAnalysisC


import sys
import json

if 2 != len(sys.argv):
    print "1 conf\nout"
    AdhocResAnalysisC().ShowConf()
    sys.exit()
    
    
    
Analysiser = AdhocResAnalysisC(sys.argv[1])


conf = cxConf(sys.argv[1])
OutName = conf.GetConf('out')
Analysiser.DrawPerQGainFigure(OutName)
print "finished"
    

