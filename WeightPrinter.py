'''
Created on Apr 5, 2013
just print weight to use in conf
@author: cx
'''
la=[0]
lb=[]
import sys

for i in range(0,5):
    la.append(0.6 + i * 0.1)
lb = la;

for a in la:
    for b in lb:
        c = 0;
        d = 1 - a - b;
        if (d < 0):
            continue;
        sys.stdout.write('%f %f %f %f\t' %(a,b,c,d))
        
