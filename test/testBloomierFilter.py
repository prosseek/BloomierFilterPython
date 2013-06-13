import unittest
import sys
sys.path.append("../src")

from bloomierFilter import *

class TestBloomierFilter(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_simple(self):
        k = {"abc":10, "def":20, "abd":30}
        bf = BloomierFilter(0, k, 10, 3, 16)

        #print "****\n\n\n"
        self.assertEqual(bf.get("abd"), k["abd"])
        self.assertEqual(bf.get("abc"), k["abc"])
        self.assertEqual(bf.get("def"), k["def"])
        self.assertEqual(bf.get("xyz"), None)
        
        bf.set("def", 12)
        self.assertEqual(bf.get("def"), 12)
        
    def test_bigTable(self):
        # hashSeed, keysDict, m, k, q
        # m should be multiple of the size m
        # k 
        # q : bit size 
        
        k = {}
        for i in range(1000):
            k[str(i)] = i
            
        m = len(k) * 2
            
        bf = BloomierFilter(0, k, m, 5, 16)
        for i in range(1000):
            self.assertEqual(bf.get(str(i)), i)
            
        # false positive
        falsePositive = 0
        for i in range(1000, 20000):
            #print bf.get(str(i))
            if bf.get(str(i)) is not None:
                falsePositive += 1
        print "# of False positive %d: %f%%" % (falsePositive, 100.0*falsePositive/(20000 - 1000))
        
if __name__ == "__main__":
    unittest.main(verbosity=2)