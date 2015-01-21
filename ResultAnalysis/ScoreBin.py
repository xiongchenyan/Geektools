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
import math,json
from operator import itemgetter

def GetBinSize(l,n=20):
    return max(math.fabs(min(l)),math.fabs(max(l))) / (n * 0.5)

def GetBinNumber(value,BinSize):
    if 0 == value:
        return 0
    BinNumber = int(math.ceil(math.fabs((value) / BinSize))) * (value / math.fabs(value))
    return BinNumber



def BinValue(l,n=20,BinSize = 0,lScore = []):
    '''
    I generate bins for score in l
    if lScore is not []
        the value in each bin will be the average of lScore (1-1 corresponding with l)
    otherwise
        bin value is count
    '''
    if 0 == BinSize:
        BinSize = GetBinSize(l,n)
    hBin = {}
        #add emtpy bin
    hBinSum = {}
    for i in range(-(n/2+1), n/2 + 2):
        if not i in hBin:
            hBin[i] = 0  
            hBinSum[i] = 0 
    for i in range(len(l)):
        value = l[i]        
        BinNumber = GetBinNumber(value,BinSize)
        if math.fabs(BinNumber) > (n/2):
            BinNumber = (n/2+1) * math.fabs(BinNumber) /BinNumber            
        hBin[BinNumber] += 1
        if [] != lScore:
            hBinSum[BinNumber] += lScore[i]
    if [] != lScore:
        for key in hBin:
            cnt = hBin[key]
            score = hBinSum[key]
            if cnt >= 1:
                hBin[key] = float(score) / cnt
            else:
                hBin[key] = 0
            
            
    lBin = [list(mid) for mid in hBin.items()]
    lBin.sort(key=itemgetter(0))
    lBinRange = GenerateBinRange(n,BinSize)
    
    for i in range(len(lBin)):
        lBin[i][0] = lBinRange[i]
    return lBin


def GenerateBinRange(n,BinSize):
    lBinRange = [] #a string based bin range name
    
#     lBinRange.append('<%.0f%%' %(100.0* (-(n/2) * BinSize)))
    lBinRange.append('')
    i = -(n/2)
    while i < n/2:
        if i == 0:
            lBinRange.append('0')
        if i < 0:
            lBinRange.append('%.0f%%' %(100.0*(i * BinSize)))
        else:
            lBinRange.append('%.0f%%' %(100.0*((i+1)*BinSize)))        
        i += 1
    lBinRange.append('%.0f%%+' %(100.0* ((n/2) * BinSize)))
    return lBinRange
