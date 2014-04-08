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






class BarPloterC(cxBaseC):
    
    def Init(self):
        self.BarWidth = 0.1
        self.ColorSeq = 'rgcbkym'
        self.XLabel = ""
        self.YLabel = ""
        self.lLegend = []
        self.XName = []
        self.X = []
        self.lY = []
        self.title = ""
        
        
    def Bar(self,OutName):
        n_group = len(self.lY)
        index = np.arange(len(self.X)) * n_group
        self.BarWidth = 1.0 / (n_group + 2) * n_group
        
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        fig, ax = plt.subplots(figsize=(9,3))
        
        ax.tick_params(axis='both',which='major',labelsize=7)
        for i in range(n_group):
            plt.bar(index + self.BarWidth * i, self.lY[i],self.BarWidth,
                    alpha=opacity,
                    color=self.ColorSeq[i%len(self.ColorSeq)],
                    error_kw=error_config,
                    label = self.lLegend[i])
        plt.xlim(index.min(), (index+self.BarWidth * n_group).max()*1.05)
        plt.xlabel(self.XLabel)
        plt.ylabel(self.YLabel)
        plt.title(self.title)
        plt.xticks(index + self.BarWidth * n_group/2.0, self.X)
        plt.legend(prop={'size':10})
        print "draw finished, saving to [%s]" %(OutName)
        plt.savefig(OutName,format='eps',dpi=1000)
        
        return True
    


    
