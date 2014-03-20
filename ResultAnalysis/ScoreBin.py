'''
Created on Mar 20, 2014
bin score automatically
@author: cx
'''


'''
input: a list of scores
output: output bins
do:
    n +1 bins default n=10
    automatically determin bin size, but max-0/0.5n
    then bin them
'''
import math
from operator import itemgetter

def GetBinSize(l,n=20):
    return max(math.fabs(min(l)),math.fabs(max(l))) / (n * 0.5)

def GetBinNumber(value,BinSize):
    if 0 == value:
        return 0
    BinNumber = int(math.ceil(math.fabs((value) / BinSize))) * (value / math.fabs(value))
    return BinNumber



def BinValue(l,n=20):
    BinSize = GetBinSize(l,n)
    hBin = {}
    for value in l:
        BinNumber = GetBinNumber(value,BinSize)
        if not BinNumber in hBin:
            hBin[BinNumber] = 0
        hBin[BinNumber] += 1
    lBin = hBin.items()
    lBin.sort(key=itemgetter(0))
    return lBin
