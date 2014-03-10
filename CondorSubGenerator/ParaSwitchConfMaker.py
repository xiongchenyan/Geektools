'''
Created on Mar 25, 2013
input: a conf and a sub file
will change the conf's paragemter, now hard coded in
and the sub file's arguments, output, error and log
@author: cx
'''



vToChangeConf = ['lambda']
vConfPara = [[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]]

import sys

#read conf in sIn
def ConfRead(sIn):
    conf={}
    for line in open(sIn):
        vCol = line.strip().split()
        if (len(vCol) < 2):
            continue
        conf[vCol[0]] = vCol[1]
    return conf

def SubRead(sIn):
    Sub={}
    for line in open(sIn):
        vCol = line.strip().split('=')
        if (len(vCol) < 2):
            continue
        Sub[vCol[0].lower()] = vCol[1]
    return Sub

#for now only modify the input and output file name in conf
def OutConfs(hConf, OutName):
    out = open(OutName,'w')
    for item in hConf:        
        print >> out, item + " " + hConf[item]
    out.close()
    return True



#now only support one dim para switch
def MakeConf(hConf,hSub):
    vName=[]
    vhConf=[]
    vhSub=[]
    global vToChangeConf
    global vConfPara
    ToChange = vToChangeConf[0]
    ParaList = vConfPara[0]
    
    for para in ParaList:
        #Name = ToChange + para
        #conf: chagne para, and out+name
        #sub: argument,out,log,error += name
        name = '_' + ToChange + '_' + str(para)
        MidConf = hConf.copy()
        MidSub = hSub.copy()
        if not (ToChange in MidConf):
            break
        MidConf[ToChange] = str(para)
        MidConf['out'] += name      
        MidSub['arguments'] += name
        MidSub['output'] += name
        MidSub['log'] += name
        MidSub['error'] += name
        
        vName.append(name)
        vhConf.append(MidConf)
        vhSub.append(MidSub)
    return vName,vhConf,vhSub


def OutAll(ConfInName,SubInName,vName,vhConf,vhSub):
    OutSub = open(SubInName + "ParaMul",'w')    
    for i in range(0,len(vName)):
        OutConfName = ConfInName + vName[i]
        OutConfs(vhConf[i],OutConfName)
        for item in vhSub[i]:
            print >> OutSub, item + "=" + vhSub[i][item]
        print >> OutSub,"queue"
    OutSub.close()


if (3 != len(sys.argv)):
    print ("2 argc: Init Conf + Init Sub")
    sys.exit()
    
hConf = ConfRead(sys.argv[1])
hSub = SubRead(sys.argv[2])

vName,vhConf,vhSub = MakeConf(hConf,hSub)
OutAll(sys.argv[1],sys.argv[2],vName,vhConf,vhSub)


     
         
        
        
            
        