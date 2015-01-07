'''
Created on Apr 2, 2014
make adhoc evaluation result table
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxConf
from ResultAnalysis.AdhocResAnalysis import AdhocResAnalysisC


import sys


if 2 != len(sys.argv):
    print "1 conf\nout"
    AdhocResAnalysisC().ShowConf()
    sys.exit()
    
Analysiser = AdhocResAnalysisC(sys.argv[1])

conf = cxConf(sys.argv[1])
caption = conf.GetConf('caption')
OutName = conf.GetConf('out')

ResStr = Analysiser.FormResTable()
out = open(OutName,'w')
print >>out,ResStr
out.close()
print "finished"
    
