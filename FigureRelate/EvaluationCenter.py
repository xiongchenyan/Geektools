'''
Created on Dec 5, 2013
evaluation root class for diversification evaluation

12/10/2013 unit test finished. evaluated alpha-NDCG20 same with TREC eval

@author: cx
'''

import sys,math,copy,json

class DivEvalC:
    def __init__(self,QRelIn = ""):
        self.hQRel = {}#key:qid-docno value: a list of tuple (st no, value, only non zeros are kept)
        self.depth = 20
        if "" != QRelIn:
            self.LoadQRel(QRelIn)

        
        
    def LoadQRel(self,QRelIn):
        #to do
        self.hQRel = {}
        for line in open(QRelIn):
            vCol = line.strip().split(' ')
            if len(vCol) != 4:
                continue
            if (vCol[3] == "0"):
                continue
            key = vCol[0] + "#" + vCol[2]
            rel = int(vCol[3])
            if rel > 1:
                rel = 1
            value = (int(vCol[1]),rel) #st no + value pair
            if not (key in self.hQRel):
                self.hQRel[key] = []
            self.hQRel[key].append(value)           
#         print "load qrel from [%s] done" %(QRelIn)
        return True
    
    def GetJudge(self,qid,DocNo):
        #get rel judgement for qid docno pair.
        #return a lSt, lSt[st no] = rel score
        key = str(qid) + "#" + DocNo
        if not key in self.hQRel:
            return []
        lSparseRel = self.hQRel[key]
        lStRel = []
        for rel in lSparseRel:
            p = rel[0]
            value = rel[1]
            if p >= len(lStRel):
                lStRel += [0] * (p - len(lStRel) + 1)
            lStRel[p] = value
        return lStRel
    
    def EvalMulQ(self,lQid,llDocRank):
        score = 0
        if (len(lQid) != len(llDocRank)):
            print "in eval mulq, doc rank len and query len nequal"
            sys.exit()
        for i in len(lQid):
            qid = lQid[i]
            lDocRank = llDocRank[i]
            score += self.EvalPerQ(qid, lDocRank)
        score /= len(lQid)
        return score
            
    
    def ShowQRel(self):
        for qrel in self.hQRel:
            print qrel + "\t" + json.dumps(self.hQRel[qrel])
            
    
    
    #lDocRank: a rank of docno
    def EvalPerQ(self,qid,lDocRank):
        print "call my sub classes"        
        return -1
    
    def GetQDocFromQRel(self):
        '''
        return a lQid, llAllDocNo pair from hQRel
        '''
        lQid = []
        hQid = {}
        llAllDocNo = []
        for qrel in self.hQRel:
            vCol = qrel.split('#')
            qid = int(vCol[0])
            doc = vCol[1]
            p = len(lQid)
            if qid in hQid:
                p = hQid[qid]
            else:
                lQid.append(qid)
                hQid[qid] = p
                llAllDocNo.append([])
            llAllDocNo[p].append(doc)
        return lQid,llAllDocNo
                
    
    
class AlphaNDCG(DivEvalC):
    
    def __init__(self,QRelIn = ""):
        DivEvalC.__init__(self,QRelIn)
        self.Init(0.5)
        
        
        
    def Init(self,alpha = 0.5):
        self.alpha = alpha
        self.hQBestDCG = {} #dict for q-best DCG
    
    def EvalPerQ(self,qid,lDocRank):
        lDocRank = lDocRank[0:self.depth]
        #to be done
        return self.__CalcAlphaNDCG(qid, lDocRank)
    
    
    def EvalMulQ(self,lQid,llDocRank):
        '''
        need to re-load DivEvalC's EvalMulQ, as a pre-calc of best dcg is required        
        '''        
        if len(self.hQBestDCG) == 0:
            self.PreCalcBestDCG()     
        score = 0
        if (len(lQid) != len(llDocRank)):
            print "in eval mulq, doc rank len and query len nequal"
            sys.exit()
        for i in range(len(lQid)):
            qid = lQid[i]
            lDocRank = llDocRank[i]
            score += self.__CalcAlphaNDCG(qid, lDocRank)
        score /= len(lQid)
        return score
        
    
    def PreCalcBestDCG(self):
        '''
        llAllDocNo are fetched from hQRel
        '''
        lQid,llAllDocNo = self.GetQDocFromQRel()
        self.hQBestDCG = {}
        llDocNo = copy.deepcopy(llAllDocNo)
        for i in range(len(lQid)):
            qid = lQid[i]
            lDocNo = llDocNo[i]        
            BestDCG = self.__CalcBestQDCG(qid, lDocNo)
            self.hQBestDCG[qid] = BestDCG
        return True
    
    def __CalcAlphaNDCG(self,qid,lRankDocNo):
        res = 0
        if not (qid in self.hQBestDCG):
            res = 0
            return res
        BestDCG = self.hQBestDCG[qid]
        if 0 == BestDCG:
            return 0
        lResDocNo = []
        lStGain = []
        lDCG = []
        
        for i in range(min(len(lRankDocNo),self.depth)):
            self.__AddToDCG(qid, lResDocNo, lStGain, lRankDocNo[i], lDCG)
        res = lDCG[len(lDCG) - 1] / BestDCG
        return res
            
    
    def __ComputeNextG(self,qid,lStGain,DocNo):
        #compute the gain of now doc no, given previous documents
        #previous documents are reflected by lStGain, [double], per subtopic penalized gain score
        #lStGain will be updated after selecting each document
        #return the G score of NowDocNo
        lPerStJ = self.GetJudge(qid, DocNo)
        if len(lStGain) < len(lPerStJ):
            lStGain += [1.0] * (len(lPerStJ) - len(lStGain))
        G = 0
        for i in range(len(lPerStJ)):
            G += lPerStJ[i] * lStGain[i]
        return G
    
    
    def __AddToDCG(self,qid,lSelectDocNo, lStGain,NowDocNo, lDCG):
        """
        Add DCG score of NowDocNo to lDCG
        qid: current query        
        lSelectDocNo: previous ranked docs, updated
        lStGain: per st penalized gain score, to be updated
        NowDocNo: to add doc no
        lDCG: dcg vector to current rank, to be updated
        return a True or False
        """
        G = self.__ComputeNextG(qid, lStGain, NowDocNo)
        DisCount = math.log(1.0 + float(len(lSelectDocNo)) + 1.0) / math.log(2.0)
        if len(lDCG) > 0:
            lDCG.append(G/DisCount + lDCG[len(lDCG) - 1])
        else:
            lDCG.append(G/DisCount)
        lSelectDocNo.append(NowDocNo)
        lPerStJ = self.GetJudge(qid, NowDocNo)
        
        if len(lStGain) < len(lPerStJ):
            lStGain += [1.0] * (len(lPerStJ) - len(lStGain))
        
        for i in range(len(lPerStJ)):
            lStGain[i] *= math.pow(1 - self.alpha, lPerStJ[i])
        return True    
        
        
    def __CalcBestQDCG(self,qid,lAllDocNo):
        '''
        calculate the best possible dcg for qid        
        return a score, as the best Alpha-NDCG, with dept set as self.depth
        '''
        lRankDocNo = []
        lStGain = []
        lDCG = []
        
        while len(lRankDocNo) < self.depth:
            MaxScore = -1
            SelectedP= -1
            if len(lAllDocNo) == 0:
                break
            for i in range(len(lAllDocNo)):
                ThisG = self.__ComputeNextG(qid, lStGain, lAllDocNo[i])
                if (ThisG > MaxScore) | (SelectedP == -1):
                    SelectedP = i
                    MaxScore = ThisG
                if (ThisG == MaxScore) & (lAllDocNo[i] > lAllDocNo[SelectedP]):
                    SelectedP = i
            self.__AddToDCG(qid, lRankDocNo, lStGain, lAllDocNo[SelectedP], lDCG)
            lAllDocNo[SelectedP] =lAllDocNo[len(lAllDocNo) - 1]
            lAllDocNo.pop()        
        if len(lDCG) == 0:
            return 0                
        return lDCG[len(lDCG) - 1]   
    
    
    
    
    
    
def LoadRankRes(InName):
    '''
    load rank res from InName (as TREC submit run result)
    to lQid and llDocRank    
    '''    
    lQid = []
    llDocRank = []
    CurrentQid = -1
    lDocRank = []
    for line in open(InName):
        vCol = line.strip().split('\t')
        qid = int(vCol[0])
        DocNo = vCol[2]
        if CurrentQid == -1:
            CurrentQid = qid            
        if qid != CurrentQid:
            llDocRank.append(lDocRank)
            lQid.append(CurrentQid)
            lDocRank = []
            CurrentQid = qid
        lDocRank.append(DocNo)
    llDocRank.append(lDocRank)
    lQid.append(CurrentQid)
    return lQid,llDocRank

def UnitTest(RankResIn,QRelIn):
    EvaCenter = AlphaNDCG()
    EvaCenter.LoadQRel(QRelIn)
#     EvaCenter.ShowQRel()
    lQid,llDocRank = LoadRankRes(RankResIn)
    EvaCenter.PreCalcBestDCG()
#     for i in range(len(lQid)):
#         print "%d\t%s" %(lQid[i],json.dumps(llDocRank[i]))    
    for i in range(len(lQid)):
        print "%d\t%f" %(lQid[i],EvaCenter.EvalPerQ(lQid[i],llDocRank[i]))
    return
        
    
    
    
    
    
    
    
        
    
