'''
Created on Mar 25, 2014

@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')


from cxBase.base import cxConf

class cxCondorC(cxConf):    
    def LoadSub(self,InName):
        for line in open(InName):
            vCol = line.strip().split("=")
            if (len(vCol) < 2):
                continue
            lConfValue = vCol[1].split(' ')
            if 1 == len(lConfValue):
                self.hConf[vCol[0].lower()] = vCol[1]
            else:
                self.hConf[vCol[0].lower()] = lConfValue #support multiple value now
        return True
    
    def LoadConf(self,InName):
        self.LoadSub(InName)
        
    def dump(self,OutName):
        out = open(OutName,'w')
        print >>out,self.dumps()
        out.close()
        return True
    
    def dumps(self):
        res = ""
        for item in self.hConf:
            value = self.hConf[item]
            if type(value) == list:
                res += item + "=" + " ".join(value) + '\n'
            else:
                res += item + "=" + value + '\n'
        res += 'queue'
        return res

            

    
    
