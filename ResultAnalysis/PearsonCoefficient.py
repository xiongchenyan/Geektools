'''
Created on Mar 20, 2014
pearson coefficient,
copied from http://snipplr.com/view/48798/pearson-correlation-coefficient/
@author: cx
'''
def pearson(x,y):
    if len(x) == 0:
        return 0
    if len(x) != len(y):
        return 0
    MeanX = sum(x)/(float(len(x)))
    MeanY = sum(y)/(float(len(y)))
    
    value = 0
    denX = 0
    denY = 0
    for i in range(len(x)):
        value += (x[i] - MeanX) * (y[i] - MeanY)
        denX += (x[i] - MeanX)**2
        denY += (y[i] - MeanY)**2
    if (denX == 0) | (denY == 0):
        return 0
    r = value / ((denX * denY)**0.5)     
    
    
    return r