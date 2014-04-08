'''
Created on Apr 2, 2014
the base class for ad hoc result analysis
input: output of ad hoc eva: each line a name\tadhocmeasurec.dump(), last line is mean
    for baseline and all methods
output:
    a table, method * measure (will add win/loss/tie and percentage for required column)
    a figure, showing per q win/lost bin compare with baseline
@author: cx
'''


'''
start with data read, conf set, and table first 4/2
figure will call python's drawer, so only able to run on my window computer

'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from AdhocEva.AdhocMeasure import *
from ScoreBin import *
from cxBase.base import *
from copy import deepcopy
from FigureRelate.BarPloter import BarPloterC

class AdhocResAnalysisC(cxBaseC):
    
    def Init(self):
        self.hBaseMeasure = {} #qid->measure
        self.lhMethodMeasure = [] #dim [method]
        self.lMethodName = []        
        self.hMainMeasure = {'err':0} #method to focus
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        lMethodName = conf.GetConf('methodname', [])
        lMethodFName = conf.GetConf('methodevares',[])
        for i in range(len(lMethodName)):
            self.LoadEvaResForMethod(lMethodFName[i],lMethodName[i])
        lMainMeasure = conf.GetConf('mainmeasure', 'err')
        if type(lMainMeasure) == list:
            self.hMainMeasure = dict(zip(lMainMeasure,range(len(lMainMeasure))))
        else:
            self.hMainMeasure[lMainMeasure] = 0
        return True
    
    @staticmethod
    def ShowConf():
        print "methodname baseline#x\nmethodevares\nmainmeasure err"
        
    
    
    def LoadEvaResForMethod(self,ResFName,MeasureName):
        lMeasure = ReadPerQEva(ResFName,True)
        hMeasure = {}
        for Measure in lMeasure:
            hMeasure[Measure[0]] = Measure[1]
        
        if MeasureName == 'baseline':
            self.hBaseMeasure = deepcopy(hMeasure)
            return True
        self.lMethodName.append(MeasureName)
        self.lhMethodMeasure.append(deepcopy(hMeasure))
        return True
    
    
    @staticmethod
    def RelativeGain(hBaseMeasure,hMeasure,MainMeasureName='err'):
        if (not 'mean' in hBaseMeasure) | (not 'mean' in hMeasure):
            print "mean value not calculate in calcing relative gain"
            return -1
        
        Base = hBaseMeasure['mean'].GetMeasure(MainMeasureName)
        Target = hMeasure['mean'].GetMeasure(MainMeasureName)
        return AdhocResAnalysisC().CalcRelGain(Base,Target)
    
    @staticmethod
    def CalcRelGain(Base,Target):
        if 0 == Base:
            return float(Target > 0)
        RelGain = Target / Base - 1.0        
        return RelGain
    
    @staticmethod
    def WinLossTie(hBaseMeasure,hMeasure,MainMeasureName='err'):
        Win = 0
        Loss = 0
        Tie = 0
        
        for item in hMeasure:
            Target = hMeasure[item].GetMeasure(MainMeasureName)
            Base = hBaseMeasure[item].GetMeasure(MainMeasureName)
            if Target > Base:
                Win += 1
            if Target == Base:
                Tie += 1
            if Target < Base:
                Loss += 1       
        
        return Win,Loss,Tie
    
    
    @staticmethod
    def WinLossNumBin(hBaseMeasure,hMeasure,MainMeasureName = 'err'):
        #get the raw relative gain number
        lRawRelGain = []
        for item in hMeasure:
            Base = hBaseMeasure[item].GetMeasure(MainMeasureName)
            Target = hMeasure[item].GetMeasure(MainMeasureName)
            lRawRelGain.append(AdhocResAnalysisC().CalcRelGain(Base, Target))
            
        #bin them to target bin
        return BinValue(lRawRelGain,n=20,BinSize=0.1)
    
    
    
    def FormResTable(self,caption='',label=''):
        #form a latex format table
        TableStr = "" #separated by \n for each row ^_^
        
        
        TableStr += self.FormResTableHead(caption, label)
        TableStr += self.FormTableRowForMethod(self.hBaseMeasure, 'baseline')
        for i in range(len(self.lhMethodMeasure)):
            hMeasure = self.lhMethodMeasure[i]
            MethodName = self.lMethodName[i]
            TableStr += self.FormTableRowForMethod(hMeasure,MethodName) 
        TableStr += self.FormTableTail()
        return TableStr 
    
    
    def FormResTableHead(self,caption = "",label = 'tab:AdHocEva'):
        
        NumOfCol = AdhocMeasureC().NumOfMeasure() + len(self.hMainMeasure)*2 + 1
        
        TableHead = "\\begin{table*}\\centering\\caption{%s\\label{%s}}" %(caption,label)
        TableHead += "\\begin{tabular}{|%s}" %('c|'*NumOfCol)
        TableHead += '\\hline\n'
        
        lMeasureName = AdhocMeasureC().MeasureName()
        TableHead += 'method'
        for MeasureName in lMeasureName:
            TableHead += "& %s" %(MeasureName)
            if MeasureName in self.hMainMeasure:
                TableHead += "& relative Gain & Win/Loss/Tie"
        TableHead += '\\\\ \\hline\n'           
        return TableHead
    
    def FormTableRowForMethod(self,hMeasure,MethodName):
        TableRow = "\\texttt{%s}" %(MethodName)
        
        for Measure in AdhocMeasureC().MeasureName():
            score = hMeasure['mean'].GetMeasure(Measure)
            TableRow += '&$%.3f$' %(score) 
            if Measure in self.hMainMeasure:
                if MethodName == 'baseline':
                    TableRow += "&NA&NA"
                else:
                    RelGain = AdhocResAnalysisC().RelativeGain(self.hBaseMeasure,hMeasure,Measure)
                    Win,Loss,Tie = AdhocResAnalysisC().WinLossTie(self.hBaseMeasure, hMeasure, Measure)
                    TableRow +="&$%.2f\\%%$ &%d/%d/%d " %(100*RelGain, Win,Loss,Tie)
        
        TableRow += '\\\\\n'              
        return TableRow
    
    def FormTableTail(self):
        TableTail = "\\hline\end{tabular}\end{table*}"
        return TableTail
    
    
    def DrawPerQGainFigure(self,FigOutName):
        #draw a per q gain figure
        #now only ploting for on target measure        
        #create X and Ys
        lY = []
        X = []
        for i in range(len(self.lMethodName)):
            lBin = self.WinLossNumBin(self.hBaseMeasure,
                                         self.lhMethodMeasure[i],
                                         self.hMainMeasure.keys()[0])
            X = [BinName for BinName,cnt in lBin]
            Y = [cnt for BinName,cnt in lBin]
            for j in range(len(X)):
                if X[j] != '0':
                    Y[j] = -Y[j]
                else:
                    break
            
            lY.append(Y)
            
            
            
        BarMaker = BarPloterC()
        BarMaker.lY = lY
        BarMaker.X = X
        BarMaker.XLabel = 'Relative Rain'
        BarMaker.YLabel = 'Number of Query'
        BarMaker.lLegend = self.lMethodName
        BarMaker.title = 'Per query relative gain'
        BarMaker.Bar(FigOutName)                
        return True
    
    
    
        
        
        


