from bloomierHasher import *
from orderAndMatch import *
from copy import *
from singletonFindingTweaker import *
from util import *

class OrderAndMatchFinder:
    def __init__(self, hashSeed, keysDict, m, k, q, maxTry = None):
        self.hashSeed = hashSeed
        self.keysDict = keysDict
        self.m = m
        self.k = k
        self.q = q
        if maxTry is None:
            self.maxTry = 5
        else:
            self.maxTry = maxTry
        
        # the list length should be len(keysDict)
        self.piList = []
        self.tauList = []
        #self.oam = OrderAndMatch(self.piList, self.tauList)
        self.hasher = BloomierHasher(hashSeed, m, k, q)
        
    def findMatch(self, remainingKeysDict):
        if len(remainingKeysDict) == 0: return True
        piTemp = []
        tauTemp = []
        
        tweaker = SingletonFindingTweaker(remainingKeysDict, self.hasher)
        for key in remainingKeysDict:
            res = tweaker.tweak(key)
            if res is not None:
                tauTemp.append(res)
                piTemp.append(key)
                
        if len(piTemp) == 0:
            return False
        
        removeAll(remainingKeysDict, piTemp)
        
        if len(remainingKeysDict) != 0:
            if self.findMatch(remainingKeysDict) == False:
                return False    
        
        addAll(self.piList, piTemp)
        addAll(self.tauList, tauTemp)
        return True
        
    def find(self):
        findIt = False;
        remainKeys = deepcopy(self.keysDict)
        # print maxTry
        for i in range(self.maxTry):
            newHashSeed = i;
            h = BloomierHasher(newHashSeed, self.m, self.k, self.q);
            remainKeys = deepcopy(remainKeys)
            if self.findMatch(remainKeys):
                # The seed value is retreived from the index
                return OrderAndMatch(i, self.piList, self.tauList)
            
if __name__ == "__main__":
    m = {"abc":10, "def":20, "abd":30}
    oamf = OrderAndMatchFinder(0, m, 10, 3, 5)
    oam = oamf.find()
    print "PILIST", oam.piList
    print "TAULIST", oam.tauList
    #print oamf.getNeighbors("abc")
    
    #oamf.findMatch(k)
    h = BloomierHasher(0, 10, 3, 5)
    t = SingletonFindingTweaker(m, h)
    key = "abc"
    print key, t.tweak(key), t.getNeighborhood(key), "\n"
    key = "abd"
    print key, t.tweak(key), t.getNeighborhood(key), "\n"
    key = "def"
    print key, t.tweak(key), t.getNeighborhood(key), "\n"
    
    # Even though key is not in the mapping, it returns value anyway
    key = "aha"
    print key, t.tweak(key), t.getNeighborhood(key), "\n"