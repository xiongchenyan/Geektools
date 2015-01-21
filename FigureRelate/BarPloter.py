'''
Created on Apr 2, 2014
plot bars
@author: cx
'''

import numpy as np
import matplotlib.pyplot as plt
import os
from cxBase.base import cxConf,cxBaseC
import json


from matplotlib import rc



class BarPloterC(cxBaseC):
    
    def Init(self):
        self.BarWidth = 0.1
        self.ColorSeq = 'rgcbkym'
        self.cpool = [ '#bd2309', '#bbb12d', '#1480fa', '#14fa2f', '#000000',
              '#faf214', '#2edfea', '#ea2ec4', '#ea2e40', '#cdcdcd',
              '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9' ]
        self.XLabel = ""
        self.YLabel = ""
        self.lLegend = []
        self.XName = []
        self.X = []
        self.lY = []
        self.title = ""
        
        
    def Bar(self,OutName,Format='eps'):
        rc('text',usetex=True)
        n_group = len(self.lY)
        index = np.arange(len(self.X)) * n_group
        self.BarWidth = 1.0 / (n_group + 2) * n_group
        
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        fig, ax = plt.subplots(figsize=(6,3.4))
        
        ax.tick_params(axis='both',which='major',labelsize=7)
        MaxY = 0
        MinY = 0
        for i in range(n_group):
            plt.bar(index + self.BarWidth * i, self.lY[i],self.BarWidth,
                    alpha=opacity,
                    color=self.cpool[i%len(self.cpool)],
                    error_kw=error_config,
                    label = r'\textbf{%s}' %(self.lLegend[i]))
            MaxY = max(MaxY,max(self.lY[i]))
            MinY = min(MinY,min(self.lY[i]))
        plt.xlim(index.min(), (index+self.BarWidth * n_group).max()*1.05)
        plt.ylim(MinY*1.5,MaxY*1.5)
        plt.xlabel(self.XLabel)
        plt.ylabel(self.YLabel)
        if self.title != "":
            plt.title(self.title)
        plt.xticks(index + self.BarWidth * n_group/2.0, self.X)
#         plt.yticks(range(int(MinY)-1,int(MaxY)+2))
        plt.legend(prop={'size':7})
        print "draw finished, saving to [%s]" %(OutName)
        plt.savefig(OutName,format=Format,dpi=1000)
        
        return True
    


    
