'''
Created on Jul 3, 2013
read adhoc evaluation results: that provided by gdeval.pl
input: EvaConf(evaresname\tmethodname + Ami Id(or you want Id) In + output summary)
output: to summary: All, AmiAll,AmiPerQ,OtherAll,OtherPerQ
@author: cx
'''

import sys
import os

def ReadAmiQid(InName):
    hAmiQid = {}
    for line in open(InName):
        Qid = (line.strip().split('\t')[0])
        hAmiQid[Qid] = True
    return hAmiQid


def ReadEvaRes(InName):
    lRes= []
    cnt = 0;
    for line in open(InName):
        if (0 == cnt):
            cnt += 1
            continue
        vCol = line.strip().split(',')
        lRes.append([vCol[1],float(vCol[2]),float(vCol[3])])
    return lRes


def SplitById(lRes,hQid):
    lIn=[]
    lOut=[]
    for res in lRes:
        if (res[0] == 'amean'):
            continue
        if (res[0] in hQid):
            lIn.append(res)
        else:
            lOut.append(res)
    return lIn,lOut


def CalcMean(lRes):
    AvgRes = ['mean',0,0]
    for res in lRes:
        AvgRes[1] += res[1]
        AvgRes[2] += res[2]
#    print "lengh of read res [%d]" %(len(lRes))
    if (len(lRes) != 0):
        AvgRes[1]/=len(lRes)
        AvgRes[2]/=len(lRes)
    return AvgRes


def WriteHead(OutDir):
    OutAll = open(OutDir+"/All","w")
    print >>OutAll,"method\tNDCG@20\tERR@20"
    OutAll.close()
    OutAmiAll = open(OutDir+"/AmiAll","w")
    print >>OutAmiAll,"method\tNDCG@20\tERR@20"
    OutAmiAll.close()
    OutOtherAll = open(OutDir + "/OtherAll",'w')
    print >> OutOtherAll, "method\tNDCG@20\tERR@20"
    OutOtherAll.close()
    OutAmiPerQ = open(OutDir + "/AmiPerQ",'w')
    print >>OutAmiPerQ,"method\tqid\tNDCG@20\tERR@20"
    OutAmiPerQ.close()
    OutOtherPerQ = open(OutDir + "/OtherPerQ",'w')
    print >>OutOtherPerQ,"method\tqid\tNDCG@20\tERR@20"
    OutOtherPerQ.close()
    return

def RunForOneMethod(EvaIn,name,OutDir,hId):
    print "working on " + EvaIn
    lRes = ReadEvaRes(EvaIn)
    lIn,lOut = SplitById(lRes,hId)
    AllAvg = CalcMean(lRes)
    InAvg= CalcMean(lIn)
    OutAvg = CalcMean(lOut)
    
    OutAll = open(OutDir+"/All","a")
    print >>OutAll,name + "\t" + str(AllAvg[1]) + "\t" + str(AllAvg[2])
    OutAll.close()
    OutAmiAll = open(OutDir+"/AmiAll","a")
    print >>OutAmiAll,name + "\t" + str(InAvg[1]) + "\t" + str(InAvg[2])
    OutAmiAll.close()
    OutOtherAll = open(OutDir+"/OtherAll","a")
    print >>OutOtherAll,name + "\t" + str(OutAvg[1]) + "\t" + str(OutAvg[2])
    OutOtherAll.close()
    
    OutAmiPerQ = open(OutDir + "/AmiPerQ",'a')
    for res in lIn:
        print >> OutAmiPerQ,name + "\t" + res[0] + "\t" + str(res[1]) + "\t" + str(res[2])
    OutAmiPerQ.close()
    OutOtherPerQ = open(OutDir + "/OtherPerQ",'a')
    for res in lOut:
        print >> OutOtherPerQ,name + "\t" + res[0] + "\t" + str(res[1]) + "\t" + str(res[2])
    OutOtherPerQ.close()
    return True


            
    


if (4 != len(sys.argv)):
    print "3 para: EvaConf + Ami(Required Id) + out dir"
    sys.exit()
    
if not os.path.exists(sys.argv[3]):
    os.makedirs(sys.argv[3])
#    print "created new dir"
    
WriteHead(sys.argv[3])
hId = ReadAmiQid(sys.argv[2])
for line in open(sys.argv[1]):
    [EvaIn,name] = line.strip().split('\t')
    RunForOneMethod(EvaIn,name,sys.argv[3],hId)
    
print "finished"
    
    

    
