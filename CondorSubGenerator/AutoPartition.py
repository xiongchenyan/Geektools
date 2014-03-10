'''
Created on Mar 13, 2013
automatically partition a input file into multiple files
as long as generate multiple conf files, and a big submit file

how to do this:
read the input file in given conf
partition it to multiple files (partition by given number of lines per file, with a main key column not separated)
for each partition file, write a conf file (with input, output modified)
(altering other conf field tbd)
and write a job queue in submit file, with argument modified to new conf, output,log,out modified,too
@author: cx


input:
conf in + sub in + KeyCol + NumOfLinePerFile
output:
will write a lot! be careful
'''

import sys

NumOfDigit = 4;

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
        Sub[vCol[0]] = vCol[1]
    return Sub

#partition input file
#return a single number, the number of output partition files
#output file's name = sIn + number (4 digit)
def PartitionFile(sIn,NumOfLinePerFile,KeyCol):
    LastKey=''
    FileNum=0
    OutCnt = 0
    global NumOfDigit
    out = open(sIn + str(FileNum).zfill(NumOfDigit),'w')
    for line in open(sIn):
        line = line.strip()
        NowKey = line.split('\t')[KeyCol]
        if ('' == LastKey):
            LastKey = NowKey
        #check if need to change file
        if (NowKey != LastKey):
            if (OutCnt > NumOfLinePerFile):
                out.close()
                OutCnt = 0
                FileNum += 1
                out = open(sIn + str(FileNum).zfill(NumOfDigit),'w')
            LastKey = NowKey
        print >>out, line
        OutCnt += 1
    out.close()
    FileNum += 1
    return FileNum


#for now only modify the input and output file name in conf
def OutConfs(hConf, NumOfOuts,OutPre):
    global NumOfDigit
    for i in range(0,NumOfOuts):
        out = open(OutPre + str(i).zfill(NumOfDigit),'w')
        for item in hConf:
            if (item =='in') | (item == 'out'):
                print >>out, item + " " + hConf[item] + str(i).zfill(NumOfDigit)
            else:
                print >> out, item + " " + hConf[item]
        out.close()
    return True
def OutSub(hSub,NumOfOuts,OutName):
    global NumOfDigit
    out = open(OutName,"w")
    ToChange = {}
    ToChange['arguments'] = True
    ToChange['output'] = True
    ToChange['log'] = True
    ToChange['error'] = True
    for i in range(0,NumOfOuts):
        for item in hSub:
            if (item.lower() in ToChange):
                print >> out, item + "=" + hSub[item] + str(i).zfill(NumOfDigit)
            else:
                print >> out, item + "=" + hSub[item]
        print >> out,"queue"
    out.close()
    return True



if 5 != len(sys.argv):
    print "4 argc: conf in + sub in + KeyCol + NumOfLinePerFile"
    sys.exit()
    
print "start read conf"    
hConf = ConfRead(sys.argv[1])
print "conf read \n start read sub"
hSub = SubRead(sys.argv[2])
print "sub read\n start partition file"
FileNum = PartitionFile(hConf['in'],int(sys.argv[4]),int(sys.argv[3]))
print "partitioned, writing confs"
OutConfs(hConf,FileNum,sys.argv[1])
print "writing sub"
OutSub(hSub,FileNum,sys.argv[2] + "MUL")
print "done"
