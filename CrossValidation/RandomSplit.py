'''
Created on Mar 7, 2014
random split
@author: cx
'''

import random,math
import json


def RandomSplit(lData,K):
    llSplit = []
    random.shuffle(lData)
    lChunks = []
    n = int(math.ceil(float(len(lData)/float(K))))
    for i in xrange(0,len(lData),n):
        lChunks.append(lData[i:i+n])
    for i in range(K):
        lTrain = []
        lTest = []
        for j in range(len(lChunks)):
            if j == i:
                lTest.extend(lChunks[j])
            else:
                lTrain.extend(lChunks[j])
        llSplit.append([lTrain,lTest])
    print "split res:\n%s"%(json.dumps(llSplit,indent=1))
    return llSplit
        
