'''
Created on Feb 23, 2015 3:55:50 PM
@author: cx

what I do:
I submit job for given commands (lCmd)
    when there is < given number of jobs (of mine) running on condor, usually 100
what's my input:
lCmd
what's my output:
I just runnign and submitting

'''

import subprocess
import time
def SimpleJobSubmitter(llCmd,MaxJob = 100):
    
    for lCmd in llCmd:
        cnt = 0
        while GetMyJobNum() >= MaxJob:
            time.sleep(10)
            cnt += 10
            print 'waiting for %d sec' %(cnt)
        print subprocess.check_output(lCmd)
        print '\t'.join(lCmd)          
    
    return True


def GetMyJobNum():
    OutStr = subprocess.check_output(['condor_q','cx'])
    lLine = OutStr.split('\n')
    return len(lLine)
