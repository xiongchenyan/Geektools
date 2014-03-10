'''
Created on Mar 28, 2013
tries to do every thing about multiple submission in condor, and close this package= =
input:
a conf file, with similar format as previously used, but for parameters need to be
switched, list all of them, to \t split
a sub file, same as before, with the given conf as input

work flow
1, do a dfs search on the conf file's parameter switch,
 generate a conf-sub pair for all combination of  parameters
2, partition the input, and for each conf-sub pair, duplicate to these multiple inputs
3, output 
@author: cx
'''


import sys
import json

FileSpliter="\t"
NumDig=4
ColToSplit = 0
NumOfLinePerFile = 20
class ConfSubC:
    name='MUL'   #the thing to add at end of file names
    hConf={}
    hSub={}
    MulParaSpliter='\t'
    
    
    ToEnumPara=[]
    ToEnumParaValue=[]
    
    def __init__(self,cB = None):
        if (cB == None):
            self.name='MUL'
            self.hConf={}
            self.hSub={}
            self.MulParaSpliter='\t'
        else:
            self.name = cB.name
            self.hConf = cB.hConf.copy()
            self.hSub = cB.hSub.copy()
            self.MulParaSpliter = cB.MulParaSpliter
    
    
    def LoadConf(self,sIn):
        self.hConf={}
        for line in open(sIn):
            vCol = line.strip().split(' ')
            if (len(vCol) < 2):
                continue
            self.hConf[vCol[0]] = " ".join(vCol[1:len(vCol)])
        return True
    def LoadSub(self,sIn):
        self.hSub={}
        for line in open(sIn):
            vCol = line.strip().split('=')
            if (len(vCol) < 2):
                continue
            self.hSub[vCol[0].lower()] = "=".join(vCol[1:len(vCol)])
        return True
    
    
    def ToEnumParaGet(self):
        self.ToEnumPara = []
        self.ToEnumParaValue = []
        for item in self.hConf:
            value = self.hConf[item]
            vCol = value.split('\t')
            if (len(vCol) < 2):
                continue
            self.ToEnumPara.append(item)
            self.ToEnumParaValue.append(vCol)
        print "To Enum Para Getted"
        print json.dumps(self.ToEnumPara)
        print json.dumps(self.ToEnumParaValue)
        return True;    
    
    #return a list of ConfSubC, one for each para meter combination
    def MulParaConfSubMaker(self):
        #make
        self.ToEnumParaGet()
        lConfSub=[]
        MidConfSub=ConfSubC(self)
        p = 0
        self.DfsMulPara(p,MidConfSub,lConfSub)
        return lConfSub
    
    def DfsMulPara(self,p,MidConfSub,lConfSub):
        #each step, foreach para in p:
            # add a substr to name
            # make midconfsub's conf corresponds to p as this para
            # call Dfs for next p
        #if ended, add name to the end of argu,log,output,error
        if (p == len(self.ToEnumPara)):
            FinalConfSub = ConfSubC(MidConfSub)
            FinalConfSub.hSub['arguments'] += FinalConfSub.name
            FinalConfSub.hSub['output'] += FinalConfSub.name
            FinalConfSub.hSub['error'] += FinalConfSub.name
            FinalConfSub.hSub['log'] += FinalConfSub.name
            FinalConfSub.hConf['out'] += FinalConfSub.name
            lConfSub.append(FinalConfSub)
            return True
        
        Para = self.ToEnumPara[p]
        for value in self.ToEnumParaValue[p]:
            name = MidConfSub.name
            MidConfSub.name += "_" + Para + "=" + value.replace(" ","-")
            MidConfSub.hConf[Para] = value
            self.DfsMulPara(p + 1,MidConfSub,lConfSub)
            MidConfSub.name = name
        return True
    
    
    #key=col
    #numofline=number per file
    #lPartionedNames if no need to partition data again, this name contains the previous 
        #partitioned result files' name
    #return a list of ConfSubC

    def MulDataPartitionConfSubMaker(self,**kwargs):
        lConfSub=[]        
        #fetch paras
        key=0
        NumOfLine = 10
        lPartionedName=[]        
        if "key" in kwargs:
            key = kwargs['key']
        if "NumOfLine" in kwargs:
            NumOfLine = kwargs['NumOfLine']
        if "lPartionedName" in kwargs:
            lPartionedName = kwargs['lPartionedName']
        
        if (len(lPartionedName) == 0):
            lPartionedName = self.PartitionInput(key, NumOfLine)
        for name in lPartionedName:
            FinalConfSub = ConfSubC(self)
            FinalConfSub.hConf['in'] += name
            FinalConfSub.hConf['out'] += name
            FinalConfSub.name += name
            FinalConfSub.hSub['arguments'] += name
            FinalConfSub.hSub['output'] += name
            FinalConfSub.hSub['error'] += name
            FinalConfSub.hSub['log'] += name
            lConfSub.append(FinalConfSub)
        return lConfSub
                 
                        
    def PartitionInput(self,col=0,NumOfLine=10):
        InName = ''
        if ('in' in self.hConf):
            InName = self.hConf['in']
        if ('input' in self.hConf):
            InName = self.hConf['input']
        if (InName == ''):
            return False;
        
        LastKey = ""
        ThisFileOutCnt = 0
        FileCnt = 0
        lName = []
        
        lName.append("_"+str(FileCnt).zfill(NumDig))
        out = open(InName + "_" + str(FileCnt).zfill(NumDig),'w')
        for line in open(InName):
            line = line.strip()
            NowKey = line.split(FileSpliter)[0]
            if (LastKey == ""):
                LastKey = NowKey
            if (NowKey != LastKey):
                if (ThisFileOutCnt >= NumOfLine):
                    out.close();
                    FileCnt += 1
                    ThisFileOutCnt = 0
                    lName.append("_" + str(FileCnt).zfill(NumDig))
                    out = open(InName + "_" + str(FileCnt).zfill(NumDig),'w')
                LastKey = NowKey
            print >> out,line
            ThisFileOutCnt += 1
        return lName
        
        
    
    def Run(self,ConfIn,SubIn):
        self.LoadConf(ConfIn)
        print "conf loaded"
        self.LoadSub(SubIn)
        print "sub loaded"
        global ColToSplit
        global NumOfLinePerFile
        lConfSub = self.MulParaConfSubMaker()
        print "Mulpara mulplication done"
        AllConfSub = []
        lFilePartName=[]
        
        for ConfSub in lConfSub:
            AllConfSub.extend(ConfSub.MulDataPartitionConfSubMaker(key=ColToSplit,NumOfLine=NumOfLinePerFile,lPartionedName=lFilePartName))
        print "mul data partition done"
        self.OutList(AllConfSub,ConfIn,SubIn)
        print "out done"
        return True
    
    def OutList(self,lConfSub,ConfIn,SubIn):
        OutSub = open(SubIn + "MULPARA",'w')
        
        for ConfSub in lConfSub:
            OutConf = open(ConfIn + ConfSub.name, 'w')
            print >> OutConf, ConfSub.ShowConf()
            OutConf.close()
            print >> OutSub, ConfSub.ShowSub()
        OutSub.close()
        return True        
        
        
    
    
    def ShowConf(self):
        s=""
        for item in self.hConf:
            s += item + " " + self.hConf[item] + "\n"
        return s.strip('\n')
    
    def ShowSub(self):
        s =""
        for item in self.hSub:
            s += item + "=" + self.hSub[item] + "\n"
        s += "queue"
        return s
    
    
        
        
        
if (3 != len(sys.argv)):
    print "conf in + sub in"
    sys.exit()

ConfSub = ConfSubC()
ConfSub.Run(sys.argv[1], sys.argv[2])
print "done"    
            