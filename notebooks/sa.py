#!/usr/bin/env python

"""
sa.py: Suffix array building and searching.

Author: Ben Langmead
Date: 1/9/2013
Contact: langmea@cs.jhu.edu
"""

from suf_tree import SuffixTree

class SuffixArray(object):
    """ Encapsulates suffix array of a string. """
    
    def __init__(self, s, sa=None, sanityChecks=False):
        self.s = s # Store string
        self.slen = len(self.s)
        if sa is not None:
            self.sa = sa
        else:
            satups = sorted([(s[i:], i) for i in xrange(0, len(s))])
            self.sa = map(lambda x: x[1], satups)
    
    @classmethod
    def fromString(cls, s, sanityChecks=False):
        return cls(s + '$', sanityChecks=sanityChecks)
    
    @classmethod
    def fromSuffixTree(cls, stree, sanityChecks=False):
        return cls(stree.s, sa=[ sa for sa in stree.sa() ], sanityChecks=sanityChecks)
    
    def first(self, p):
        """ Return 1st SA element with p as a prefix if such element
            exists, or the offset where it would be otherwise. """
        L, R = 0, self.slen - 1
        while R - L > 1:
            M = (L + R) / 2
            bisectLeft = True
            for i in xrange(0, len(p)):
                if p[i] < self.s[self.sa[M] + i]:
                    break
                elif p[i] > self.s[self.sa[M] + i]:
                    bisectLeft = False
                    break
            if bisectLeft: R = M
            else:          L = M
        if R == self.slen-1 and p > self.s[self.sa[R]:]:
            return self.slen # special case: fell off right-hand side
        return R
    
    def range(self, p):
        """ Return the range of suffix array rows having p as a prefix,
            or empty range if no elements have p as a prefix.
            Right-hand extreme is exclusive. """
        pp = p[:-1]
        pp += chr(ord(p[-1])+1) # pp = string just a bit greater than p
        l, r = self.first(p), self.first(pp)
        return l, r
    
    def range2(self, p):
        """ Find range of suffix array elements that have p as a prefix """
        l = 0
        r = len(self.s)+1
        # bisect until l points at first element with p as prefix
        while l < r:
            mid = (l+r) / 2
            midsa = self.sa[mid]
            if p > self.s[midsa:midsa+len(p)]:
                l = mid + 1
            else:
                r = mid
        s = l # save l, which is the final l
        # bisect until r points just below final element with p as prefix
        r = len(self.s)+1
        while l < r:
            mid = (l+r) / 2
            midsa = self.sa[mid]
            if p == self.s[midsa:midsa+len(p)]:
                if l == mid:
                    break
                l = mid
            else:
                r = mid
        return (s, r)
    
    def rangeCount(self, p):
        """ Find range of suffix array elements that have p as a prefix """
        l = 0
        r = len(self.s)+1
        ncmp = 0
        # bisect until l points at first element with p as prefix
        while l < r:
            mid = (l+r) / 2
            assert mid != r
            print (m, l, r)
            midsa = self.sa[mid]
            gt = False
            for i in xrange(0, len(p)):
                ncmp += 1
                if p[i] > self.s[midsa + i]:
                    gt = True
                    break # bisect!
                elif p[i] < self.s[midsa + i]:
                    break # bisect!
            if gt:
                l = mid + 1
            else:
                r = mid
        s = l # save l, which is the final l
        # bisect until r points just below final element with p as prefix
        r = len(self.s) + 1
        while l < r:
            mid = (l+r) / 2
            assert mid != r
            print (m, l, r)
            midsa = self.sa[mid]
            equ = True
            for i in xrange(0, len(p)):
                ncmp += 1
                if p[i] != self.s[midsa + i]:
                    equ = False
                    break # bisect!
            if equ:
                if l == mid:
                    break # bisect!
                l = mid
            else:
                r = mid
        return (s, r, ncmp)
    
    def hasSubstring(self, p):
        """ Return true if and only if p is substring of indexed text """
        l, r = self.range(p)
        return r > l
    
    def hasSuffix(self, p):
        """ Return true if and only if p is suffix of indexed text """
        l, r = self.range(p)
        return r > l and self.sa[l] + len(p) == self.slen-1
    
    def toBwt(self):
        """ Convert suffix array to BWT string, along with row where $ occurs
            (i.e. i s.t. SA[i] = 0) """
        bw = []
        dollarRow = None
        for si in self.sa:
            if si == 0:
                dollarRow = len(bw)
                bw.append('$')
            else:
                bw.append(self.s[si-1])
        assert dollarRow is not None
        return (''.join(bw), dollarRow) # return string-ized version of list bw
    
    def toIsa(self, upto=None):
        """ Convert suffix array to inverse suffix array """
        pass
    
    def sampleByRank(self, e):
        """ Generate a sample of the suffix array where we take suffixes with
            ranks = 0 mod e. """
        for i in xrange(0, len(self.s)):
            if self.sa[i] % e == 0:
                yield i, self.sa[i]

if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
    
        def test_search_1(self):
            for fromStree in (True, False):
                sa = SuffixArray.fromSuffixTree(SuffixTree("abaaba")) if fromStree else SuffixArray.fromString("abaaba")
                self.assertTrue(sa.hasSubstring("aaba"))
                self.assertFalse(sa.hasSubstring("aabb"))
                l = sa.first("a")
                self.assertEqual(1, l)
                l = sa.first("b")
                self.assertEqual(5, l)
                l, r = sa.range("a")
                self.assertEqual(1, l)
                self.assertEqual(5, r)
                l, r = sa.range("b")
                self.assertEqual(5, l)
                self.assertEqual(7, r)
                l, r = sa.range("ba")
                self.assertEqual(5, l)
                self.assertEqual(7, r)
                l, r = sa.range("baaba")
                self.assertEqual(6, l)
                self.assertEqual(7, r)
                self.assertTrue(sa.hasSubstring("abaaba"))
                self.assertTrue(sa.hasSubstring("baaba"))
                self.assertTrue(sa.hasSubstring("aaba"))
                self.assertTrue(sa.hasSubstring("abaab"))
                self.assertTrue(sa.hasSubstring("abaa"))
                self.assertTrue(sa.hasSuffix("aba"))
                self.assertTrue(sa.hasSuffix("ba"))
                self.assertTrue(sa.hasSuffix("a"))
                self.assertFalse(sa.hasSubstring("abc"))
                self.assertFalse(sa.hasSubstring("abaabaa"))
                self.assertFalse(sa.hasSubstring("ababa"))
                self.assertFalse(sa.hasSubstring("z"))
                self.assertFalse(sa.hasSubstring("zzzzzz"))

        def test_search_2(self):
            for fromStree in (True, False):
                sa = SuffixArray.fromSuffixTree(SuffixTree("acgtacgtacgtacgt")) if fromStree else SuffixArray.fromString("acgtacgtacgtacgt")
                self.assertFalse(sa.hasSuffix("ab"))
                self.assertFalse(sa.hasSubstring("aa"))
                self.assertFalse(sa.hasSubstring("zz"))
                self.assertTrue(sa.hasSuffix("acgt"))
    
    import sys
    unittest.main(argv=[sys.argv[0]])
    sys.exit()
