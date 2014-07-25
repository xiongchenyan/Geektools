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
from StatisticSignificantTest import *
class AdhocResAnalysisC(cxBaseC):
    
    def Init(self):
        self.hBaseMeasure = {} #qid->measure
        self.lhMethodMeasure = [] #dim [method], each dimension is a evaluation result dict (qid->measure)
        self.lMethodName = []        
        self.hMainMeasure = {'err':0} #method to focus
        
        self.TestCenter = FisherRandomizationTestC()
        self.lTestSign = ["\\dagger","\\ddagger","\\mathsection","\\mathparagraph"] #latex sign for significant label
        self.lTestName = []
        self.llStatTestRes = []
        self.Caption = ""
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        lMethodName = conf.GetConf('methodname', [])
        lMethodFName = conf.GetConf('methodevares',[])
        for i in range(len(lMethodName)):
            self.LoadEvaResForMethod(lMethodFName[i],lMethodName[i])
        print "add non present q baseline value"
        self.AddBaselineQPerform()

        '''
        fill all methods' empty qid result by baseline's TBD
        '''    
        for i in range(len(self.lhMethodMeasure)):
            self.lhMethodMeasure[i] = AdhocMeasureC.FillMissEvaByBaseline(self.lhMethodMeasure[i], self.hBaseMeasure)    
            print "len [%d]" %(len(self.lhMethodMeasure[i]))          
           
        lMainMeasure = conf.GetConf('mainmeasure', 'err')
        if type(lMainMeasure) == list:
            self.hMainMeasure = dict(zip(lMainMeasure,range(len(lMainMeasure))))
        else:
            self.hMainMeasure[lMainMeasure] = 0
        self.TestCenter.SetConf(ConfIn)
        self.Caption = conf.GetConf('caption')
        return True
    
    @staticmethod
    def ShowConf():
        print "methodname baseline#x\nmethodevares\nmainmeasure err\ncaption"
        
    
    
    def LoadEvaResForMethod(self,ResFName,MeasureName):
        lMeasure = AdhocMeasureC.ReadPerQEva(ResFName,True)
        hMeasure = {}
        for Measure in lMeasure:
            hMeasure[Measure[0]] = Measure[1]
        
        if MeasureName == 'baseline':
            self.hBaseMeasure = deepcopy(hMeasure)
            return True
        self.lMethodName.append(MeasureName)
        self.lhMethodMeasure.append(deepcopy(hMeasure))
        return True
    
    def AddBaselineQPerform(self):
        
        for hMeasure in self.lhMethodMeasure:
            for item in self.hBaseMeasure:
                if not item in hMeasure:
                    hMeasure[item] = self.hBaseMeasure[item]
            Total = AdhocMeasureC()
            Cnt = 0
            for item,value in hMeasure.items():
                if item != 'mean':
                    Total += value
                    Cnt += 1.0
            if Cnt != 0:
                hMeasure['mean'] = Total / Cnt
            
    
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
        RandomBase = 0.01
        if 0 == Base:
            return float(Target > 0)
        RelGain = Target / Base - 1.0
        if abs(RelGain) < RandomBase:
            RelGain = 0        
        return RelGain
    
    @staticmethod
    def WinLossTie(hBaseMeasure,hMeasure,MainMeasureName='err'):
        Win = 0
        Loss = 0
        Tie = 0
        RandomBase = 0.01
        for item in hMeasure:
            if 'mean' == item:
                continue
            Target = hMeasure[item].GetMeasure(MainMeasureName)
            Base = hBaseMeasure[item].GetMeasure(MainMeasureName)
            
#             if (Base != 0):
#                 if (abs(float(Target - Base)/Base) < RandomBase):
#                     Tie += 1
#                     continue
            if Target > Base:
                Win += 1
            if Target == Base:
                Tie += 1
            if Target < Base:
                Loss += 1       
        
        return Win,Loss,Tie
    
    def WinLossTieTable(self,lEvaMethodName):
        '''
        form win loss tie table for methods in eva method name
        '''
        lName = []
        lPos = []
        #get position
        for name in lEvaMethodName:
            if not name in self.lMethodName:
                continue
            pos = self.lMethodName.index(name)
            lPos.append(pos)
            lName.append(name)
        
        
        FullTable = ""    
        TableHead = ""
        
        NumOfCol = len(lName) + 1
        TableHead += "\\begin{table*}\\centering\\caption{ \label{tab. }}\n"
        TableHead += "\\begin{tabular}{|%s}\n" %('c|'*NumOfCol)
        TableHead += '\\hline\n'
        
        for i in range(len(lName)):
            TableHead += "& \\texttt{%s}" %(lName[i])
        TableHead += '\\\\ \\hline\n'
        
        
        FullTable += TableHead + "\n"
        for i in range(len(lName)):
            TableRow = "\\texttt{%s}" %(lName[i])
            for j in range(len(lName)):
                if j == i:
                    TableRow += "& NA/NA/NA"
                    continue
                Win,Loss,Tie = AdhocResAnalysisC.WinLossTie(self.lhMethodMeasure[lPos[j]], self.lhMethodMeasure[lPos[i]])
                TableRow += "&%d/%d/%d" %(Win,Loss,Tie)
            TableRow += '\\\\\n'
            FullTable += TableRow
        
        FullTable += '\\hline\end{tabular}\end{table*}'
        
        return FullTable
          
            
        
    
    @staticmethod
    def WinLossNumBin(hBaseMeasure,hMeasure,MainMeasureName = 'err'):
        #get the raw relative gain number
        lRawRelGain = []
        for item in hMeasure:
            if item == 'mean':
                continue
            Base = hBaseMeasure[item].GetMeasure(MainMeasureName)
            Target = hMeasure[item].GetMeasure(MainMeasureName)
            lRawRelGain.append(AdhocResAnalysisC().CalcRelGain(Base, Target))
            
        #bin them to target bin
        return BinValue(lRawRelGain,n=10,BinSize=0.2)
    
    
    
    def PerformStatisTest(self):
        '''
        read and perform statistic test, by class in StatiticSigificant test, store in self.llStatTestRes (method * baseline method, p)
        will be used in form res table row for method
        '''
        print "performing stat test"
        self.lTestName,self.llStatTestRes = self.TestCenter.Process()
        return self.lTestName,self.llStatTestRes
    
    def FetchTestRes(self,MethodName,Measure):
        Pos = self.lTestName.index(MethodName)
        lRes = self.llStatTestRes[Pos]
        TestSignStr = ""
        if len(lRes) > len(self.lTestSign):
            print 'need more test sign [%d] < [%d]' (len(self.lTestSign) < len(lRes))
        for i in range(len(lRes)):
            pvalue = lRes[i].GetMeasure(Measure)
            print "measure [%s][%s] p = [%s] vs No. [%d] baseline" %(MethodName,Measure,pvalue,i)
            if pvalue < 0.05:
                TestSignStr += self.lTestSign[i] + ','
                
        return TestSignStr.strip(',')
                
            
    
    
    def FormResTable(self,caption='',label=''):
        #form a latex format table
        if caption == '':
            caption = self.Caption
        self.PerformStatisTest()
        
        TableStr = "" #separated by \n for each row ^_^
        
        
        TableStr += self.FormResTableHead(caption, label)
        TableStr += self.FormTableRowForMethod(self.hBaseMeasure, 'baseline')
        for i in range(len(self.lhMethodMeasure)):
            hMeasure = self.lhMethodMeasure[i]
            MethodName = self.lMethodName[i]
            TableStr += self.FormTableRowForMethod(hMeasure,MethodName) 
        TableStr += self.FormTableTail()
        return TableStr 
    
    
    def FormResTableHead(self,caption = '',label = 'tab:AdHocEva'):
        if caption == '':
            caption = self.Caption
        NumOfCol = AdhocMeasureC().NumOfMeasure() + len(self.hMainMeasure)*2 + 1
        TableHead = "\\begin{table*}\\centering\\caption{%s\\label{%s}}\n" %(caption,label)
        TableHead += "\\begin{tabular}{|%s}\n" %('l|'*NumOfCol)
        TableHead += '\\hline\n'
        
        lMeasureName = AdhocMeasureC().MeasureName()
        TableHead += 'Method'
        for MeasureName in lMeasureName:
            TableHead += "& %s" %(MeasureName.upper())
            if MeasureName in self.hMainMeasure:
                TableHead += "& Relative Gain & Win/Loss/Tie"
        TableHead += '\\\\ \\hline\n'           
        return TableHead
    
    def FormTableRowForMethod(self,hMeasure,MethodName):
        TableRow = "\\texttt{%s}" %(MethodName)
        
        for Measure in AdhocMeasureC().MeasureName():
            score = hMeasure['mean'].GetMeasure(Measure)
            TestStr = self.FetchTestRes(MethodName,Measure)
            '''
            add significant test result here
            '''
            TableRow += '&$%.3f^{%s}$' %(score,TestStr) 
           
            
            
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
        '''
        #draw a per q gain figure
        #now only ploting for on target measure        
        #create X and Ys
        '''
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
        BarMaker.XLabel = 'Relative Gain'
        BarMaker.YLabel = 'Number of Query'
        BarMaker.lLegend = self.lMethodName
        BarMaker.title =  self.Caption
        BarMaker.Bar(FigOutName)                
        return True
    
    
    
        
        
        


