'''
Created on Apr 23, 2014
split data by key
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')

from CrossValidation.FoldNameGenerator import *
from cxBase.KeyFileReader import KeyFileReaderC
import sys
from cxBase.base import cxConf
import gzip
def ShowConf():
    print "in\nrootdir\nK\nkeyindex 0\ngzip false"
    
    
    
if 2 != len(sys.argv):
    print "1 conf:"
    ShowConf()
    sys.exit()


conf = cxConf(sys.argv[1])
Namer =  FoldNameGeneratorC(sys.argv[1])   

InName = conf.GetConf('in')
K = int(conf.GetConf('K'))
KeyIndex = int(conf.GetConf('keyindex'))
UseGzip = bool(conf.GetConf('gzip','true'))

#read num of key
KeyReader = KeyFileReaderC()
KeyReader.KeyIndex = KeyIndex
KeyReader.UseGzip = UseGzip
KeyReader.open(InName)

print "cnting key"
KeyCnt = 0
for lvCol in KeyReader:
    KeyCnt += 1
    if 0 == (KeyCnt % 10000):
        print "cnt [%d] key" %(KeyCnt)
    
    
KeyReader.close()


print "total [%d] key" %(KeyCnt)
N = int(math.ceil(float(KeyCnt) / K))
print "each fold [%d] key" %(N)
OutCnt = 0
if UseGzip:
    out = gzip.open(Namer.DataDir() + "/test_%d" %(OutCnt),'w')
else:
    out = open(Namer.DataDir() + "/test_%d" %(OutCnt),'w')

cnt = 0


KeyReader.open(InName)
print "start spliting"
for lvCol in KeyReader:
    for vCol in lvCol:
        print >> out,"\t".join(vCol)
    cnt += 1
    if cnt >= N:
        out.close()
        print "split [%d] done" %(OutCnt)
        OutCnt += 1
        out = open(Namer.DataDir() + "/test_%d" %(OutCnt),'w')
        cnt = 0
        
out.close()
print "finished"
        
        