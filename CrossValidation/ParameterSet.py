'''
Created on Mar 9, 2014
A Parameter set class (in GeekTools.CV package):
    read conf and general list of parameters, (combination of parameters)
    stored in a {parameter name:value}
@author: cx
'''


from cxBase.base import *
import copy

class ParameterSetC:
    def Init(self):
        self.hPara = {} #mapping from paraname to value
        return
    
    def __init__(self):
        self.Init()
    
    
    def __deepcopy__(self,memo):
        NewPara = ParameterSetC()
        NewPara.hPara = copy.deepcopy(self.hPara, memo)
        return NewPara    
        
        
        
        
def ReadParaSet(ConfIn):
    #read para set from conf
        #format: name value#value#value
        #if value if string, then use "", otherwise should be float
    lParameterSet = []
    conf = cxConf.LoadConf(ConfIn)
    lName = []
    llValue = []
    for para in conf.hConf:
        value = conf.hConf[para]
        if type(value) == list:
            llValue.append(value)
        else:
            llValue.append([value])
            
    #convert llValue
    for i in range(len(llValue)):
        for j in range(len(llValue[i])):
            if llValue[i][j][0] == '"':
                continue
            try:
                llValue[i][j] = float(llValue[i][j])
            except ValueError:
                pass
            
    #dfs enumerate to generate para set
    DFSEnumerateParaSet(lName,llValue,lParameterSet)    
    return lParameterSet



def DFSEnumerateParaSet(lName,llValue,lParameterSet,CurParaSet=ParameterSetC(),CurLvl=0):
    if CurLvl >= len(lName):
        #end of dfs, yield parameter, need a deep copy and put to lParameterSet
        lParameterSet.append(copy.deepcopy(CurParaSet))
        return True
    
    name = lName[CurLvl]
    lValue = llValue[CurLvl]
    for i in range(len(lValue)):        
        CurParaSet.hPara[name] = lValue[i]
        DFSEnumerateParaSet(lName,llValue,lParameterSet,CurParaSet,CurLvl+1)           
    return True
                
            
        
        
    
