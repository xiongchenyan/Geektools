'''
Created on Nov 18, 2013
print para file and sub for freebase
@author: cx
'''


import sys


if (3 > len(sys.argv)):
    print "2 argv: para file out pre + subcondor file out name"
    print "or 3 argv: para file out pre + subcondor file out name + stopword list"
    sys.exit()

NumOfPartition = 10

bUseStopWord = False
if 4 == len(sys.argv):
    bUseStopWord = True
    
sStopWord = ""
for line in open(sys.argv[3]):
    sStopWord += line
    


for i in range(0,NumOfPartition):
    out = open("MulPara" + sys.argv[1] + str(i),'w')
    print >> out,"<parameters>\n<corpus>"
    print >> out, "<path>/bos/tmp17/cx/Freebase/TextTrecWebFormat/%s</path>" %(i)
    print >> out, "<class>trecweb</class>\n </corpus>\n<stemmer><name>Krovetz</name></stemmer>"
    print >> out, "<memory>1G</memory>"
    print >> out, "<index>/bos/tmp17/cx/Freebase/%s/%d</index>" %(sys.argv[1],i)
    print >> out, "<metadata><field>key</field></metadata>"
    print >> out, "<metadata><field>name</field></metadata>"
    print >> out, "<metadata><field>description</field></metadata>"
    print >> out, "<metadata><field>content</field></metadata>"
    print >> out, "<metadata><field>docno</field></metadata>"
    print >> out, "<metadata><field>mid</field></metadata>"
    print >> out, "<metadata><field>link</field></metadata>"
    print >> out, "<field><name>key</name></field>"
    print >> out, "<field><name>name</name></field>"
    print >> out, "<field><name>description</name></field>"
    print >> out, "<field><name>content</name></field>"
    print >> out, "<field><name>docno</name></field>"
    print >> out, "<field><name>mid</name></field>"
    print >> out, "<field><name>link</name></field>"
    if bUseStopWord:
        print >> out, sStopWord
    print >> out, "</parameters>"
    out.close()


out = open(sys.argv[2], "w")
print >> out,"universe=vanilla"
for i in range(0,NumOfPartition):
    print >> out,"Executable=/bos/usr4/cx/Freebase/IndexingFreebase/IndriBuildIndex"
    print >> out,"Arguments=/bos/usr4/cx/Freebase/IndexingFreebase/%s" %("MulPara" + sys.argv[1]+str(i))
    print >> out,"Log=/bos/tmp17/cx/log/BuildIndexFbMul%d.log" %(i)
    print >> out,"output=/bos/tmp17/cx/log/BuildIndexFbMul%d.out" %(i)
    print >> out,"error=/bos/tmp17/cx/log/BuildIndexFbMul%d.error" %(i)
    print >> out, "Queue"

out.close()
