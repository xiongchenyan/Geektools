'''
Created on Apr 2, 2014
plot bars
@author: cx
'''

import numpy as np
import matplotlib.pyplot as plt
import os
from cxBase.base import cxConf,cxBaseC







class BarPloterC(cxBaseC):
    
    def Init(self):
        self.BarWidth = 0.1
        self.ColorSeq = 'rgbkymc'
        self.XLabel = ""
        self.YLabel = ""
        self.lLegend = []
        self.XName = []
        self.X = []
        self.lY = []
        self.title = ""
        
        
    def Bar(self,OutName):
        n_group = len(self.lY)
        index = np.arange(n_group)
        self.BarWidth = 1.0 / (n_group + 2)
        
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        fig, ax = plt.subplots()
        
        
        for i in range(n_group):
            plt.bar(index + self.BarWidth * i, self.lY[i],self.BarWidth,
                    alpha=opacity,
                    color=self.ColorSeq[i%len(self.ColorSeq)],
                    error_kw=error_config,
                    label = self.lLegend[i])
        plt.xlabel(self.XLabel)
        plt.ylabel(self.YLabel)
        plt.title(self.title)
        plt.xticks(index + self.BarWidth * n_group/2.0, self.X)
        plt.legend()
        
        plt.savefig(OutName,format='eps',dpi=1000)
        
        return True
    


    
