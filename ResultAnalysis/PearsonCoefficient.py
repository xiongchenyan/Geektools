'''
Created on Mar 20, 2014
pearson coefficient,
copied from http://snipplr.com/view/48798/pearson-correlation-coefficient/
@author: cx
'''
def pearson(x,y):
    n=len(x)
    vals=range(n)
 
    #regular sums
    sumx=sum([float(x[i]) for i in vals])
    sumy=sum([float(y[i]) for i in vals])
 
    #sum of the squares
    sumxSq=sum([x[i]**2.0 for i in vals])
    sumySq=sum([y[i]**2.0 for i in vals])
 
    #sum of the products
    pSum=sum([x[i]*y[i] for i in vals])
 
    #do pearson score
    num=pSum-(sumx*sumy/n)
    den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)))**.5
    if den==0:
        return 1
    r=num/den
    return r