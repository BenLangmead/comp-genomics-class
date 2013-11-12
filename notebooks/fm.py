#!/usr/bin/env python

"""
fm.py: FM Index implementation with O(1)-spaced checkpoints and suffix array
       samples, and O(n) queries.

Author: Ben Langmead
Date: 2/23/2013
Contact: langmea@cs.jhu.edu
"""

from sa import SuffixArray
from suf_tree import SuffixTree

def rotations(t):
    """ Return list of rotations of input string t """
    tt = t * 2
    return [ tt[i:i+len(t)] for i in xrange(0, len(t)) ]

def bwm(t):
    """ Return lexicographically sorted list of rotations of t """
    return sorted(rotations(t))

def naive(p, t, start=0, end=None):
    
    """ Naive exact matching algorithm """
    
    if end is None:
        end = len(t) - len(p) + 1
    matches = []
    for i in xrange(start, end):
        for j in xrange(0, len(p)):
            if t[i+j] != p[j]:
                break # next attempt
        else:
            matches.append(i) # match
    return matches

def suffixArray(s):
    """ Given T return suffix array SA(T).  We use Python's sorted
        function here for simplicity, but we can do better. """
    satups = sorted([(s[i:], i) for i in xrange(0, len(s))])
    # Extract and return just the offsets
    return map(lambda x: x[1], satups)

def downsampleSuffixArray(sa, n=4):
    """ Take only the suffix-array entries for every nth suffix.  Keep
        suffixes at offsets 0, n, 2n, etc.  Return map from the rows we
        kept to their suffix-array values. """
    ssa = {}
    for i in xrange(0, len(sa)):
        # We could use i % n instead of sa[i] % n, but we lose the
        # constant-time guarantee for resolutions
        if sa[i] % n == 0:
            ssa[i] = sa[i]
    return ssa

def bwtFromSa(t, sa=None):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    dollarRow = None
    if sa is None:
        sa = suffixArray(t)
    for si in sa:
        if si == 0:
            dollarRow = len(bw)
            bw.append('$')
        else:
            bw.append(t[si-1])
    assert dollarRow is not None
    return (''.join(bw), dollarRow) # return string-ized version of list bw

class FmCheckpoints(object):
    """ Manages rank checkpoints, handles rank queries, which are O(1) """
    
    def __init__(self, bw, cpIval=4):
        """ Scan BWT, creating checkpoints as we go """
        self.cps = {}        # checkpoints
        self.cpIval = cpIval # spacing between checkpoints
        tally = {}           # tally so far
        for c in bw:
            if c not in tally:
                tally[c] = 0
                self.cps[c] = []
        for i in xrange(0, len(bw)):
            tally[bw[i]] += 1
            if (i % cpIval) == 0:
                for c in tally.iterkeys():
                    self.cps[c].append(tally[c])
    
    def rank(self, bw, c, row):
        """ Return c's rank w/r/t 'row'.  I.e., how many c's are there in rows
            up to and including 'row'. """
        if row < 0 or c not in self.cps:
            return 0
        i = row
        nocc = 0
        while (i % self.cpIval) != 0:
            if bw[i] == c:
                nocc += 1
            i -= 1
        rank = self.cps[c][i / self.cpIval] + nocc
        return rank

class FmIndex():
    
    def __init__(self, t=None, cpIval=4, ssaIval=4, sa=None):
        if t is not None and t[-1] != '$':
            t += '$'
        if t is None and sa is None:
            raise RuntimeError("Either t or sa must be specified")
        if sa is None:
            sa = suffixArray(t)
            self.bwt, self.dollarRow = bwtFromSa(t, sa)
            self.ssa = downsampleSuffixArray(sa, ssaIval)
        else:
            self.bwt, self.dollarRow = sa.toBwt()
            self.ssa = {}
            for off, sa in sa.sampleByRank(ssaIval):
                self.ssa[off] = sa
        self.slen = len(self.bwt)
        self.cps = FmCheckpoints(self.bwt, cpIval)
        # Calculate total # of each character
        tots = dict()
        for c in self.bwt:
            tots[c] = tots.get(c, 0) + 1
        # Calculate concise representation of first column
        self.first = {}
        totc = 0
        for c, count in sorted(tots.iteritems()):
            self.first[c] = totc
            totc += count
    
    @classmethod
    def fromString(cls, s, cpIval=4, ssaIval=4):
        return cls(t=s + '$', cpIval=cpIval, ssaIval=ssaIval)
    
    @classmethod
    def fromSuffixArray(cls, sa, cpIval=4, ssaIval=4):
        return cls(sa=sa, cpIval=cpIval, ssaIval=ssaIval)
    
    @classmethod
    def fromSuffixTree(cls, stree, cpIval=4, ssaIval=4):
        return FmIndex.fromSuffixArray(SuffixArray.fromSuffixTree(stree), cpIval=cpIval, ssaIval=ssaIval)
    
    def count(self, c):
        """ Count number of occurrences of characters < c """
        if c not in self.first:
            for cc in sorted(self.first.iterkeys()):
                if c < cc:
                    return self.first[cc]
            return self.first[cc]
        else: return self.first[c]
    
    def range(self, p):
        """ Return the range of BWM rows having p as a prefix """
        l, r = 0, self.slen - 1
        for i in xrange(len(p)-1, -1, -1):
            c = p[i]
            l, r = self.nextRange(l, r+1, c)
            r -= 1
            if r < l:
                break
        return l, r+1
    
    def nextRange(self, l, r, c):
        ''' If l, r is a right-open range of BWM rows having p as a
            prefix, this returns newl, newr, a right-open range of BWM
            rows with c + p as a prefix.  '''
        l = self.cps.rank(self.bwt, c, l-1) + self.count(c)
        r = self.cps.rank(self.bwt, c, r-1) + self.count(c)
        return l, r
    
    def stepLeft(self, row, c=None):
        """ Step left according to character in given BWT row """
        assert row < len(self.bwt)
        if c is None: c = self.bwt[row]
        return self.cps.rank(self.bwt, c, row-1) + self.count(c)
    
    def resolve(self, row):
        """ Given BWM row, return its offset w/r/t T """
        nsteps = 0
        while row not in self.ssa:
            row = self.stepLeft(row)
            nsteps += 1
        return self.ssa[row] + nsteps
    
    def hasSubstring(self, p):
        """ Return true if and only if p is substring of indexed text """
        l, r = self.range(p)
        return r > l
    
    def hasSuffix(self, p):
        """ Return true if and only if p is suffix of indexed text """
        l, r = self.range(p)
        off = self.resolve(l)
        return r > l and off + len(p) == self.slen-1
    
    def occurrences(self, p):
        """ Return offsets for all occurrences of p, in no particular order """
        l, r = self.range(p)
        return [ self.resolve(x) for x in xrange(l, r) ]

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Do Naive exact matching on arguments')
    
    parser.add_argument(\
        '--text', metavar='string', type=str, help='Text T')
    parser.add_argument(\
        '--dot', metavar='path', type=str, help='Write dot output to PDF file')
    parser.add_argument(\
        '--string-lab', action='store_const', const=True, default=False, help='Use strings on edge labels for --dot')
    parser.add_argument(\
        '--text-file', metavar='path', type=str, help='File containing text T')
    parser.add_argument(\
        '--text-ignore-ws', action='store_const', const=True, default=False, help='Ignore whitespace in text')
    parser.add_argument(\
        '--text-uppercase', action='store_const', const=True, default=False, help='Make text all-uppercase')
    parser.add_argument(\
        '--test', action='store_const', const=True, default=False, help='Do unit tests')
    
    args = parser.parse_args()
    
    if args.test:
        import sys
        import unittest
        
        def constructions(s):
            return [ FmIndex.fromString(s),
                     FmIndex.fromSuffixArray(SuffixArray.fromString(s)),
                     FmIndex.fromSuffixTree(SuffixTree(s)) ]
        
        class Test(unittest.TestCase):
            
            def test_cp_1(self):
                bw = "acgtacgt$"
                for i in xrange(1, len(bw)):
                    cp = FmCheckpoints(bw, i)
                    self.assertEquals(1, cp.rank(bw, 'a', 0))
                    self.assertEquals(0, cp.rank(bw, 'c', 0))
                    self.assertEquals(0, cp.rank(bw, 'g', 0))
                    self.assertEquals(0, cp.rank(bw, 't', 0))
                    self.assertEquals(0, cp.rank(bw, '$', 0))
                    
                    self.assertEquals(1, cp.rank(bw, 'a', 1))
                    self.assertEquals(1, cp.rank(bw, 'c', 1))
                    self.assertEquals(0, cp.rank(bw, 'g', 1))
                    self.assertEquals(0, cp.rank(bw, 't', 1))
                    self.assertEquals(0, cp.rank(bw, '$', 1))
                    
                    self.assertEquals(1, cp.rank(bw, 'a', 2))
                    self.assertEquals(1, cp.rank(bw, 'c', 2))
                    self.assertEquals(1, cp.rank(bw, 'g', 2))
                    self.assertEquals(0, cp.rank(bw, 't', 2))
                    self.assertEquals(0, cp.rank(bw, '$', 2))
                    
                    self.assertEquals(2, cp.rank(bw, 'a', 4))
                    self.assertEquals(1, cp.rank(bw, 'c', 4))
                    self.assertEquals(1, cp.rank(bw, 'g', 4))
                    self.assertEquals(1, cp.rank(bw, 't', 4))
                    self.assertEquals(0, cp.rank(bw, '$', 4))
                    self.assertEquals(0, cp.rank(bw, 'X', 4))
            
            def test_search_1(self):
                for fm in constructions("abaaba"):
                    self.assertFalse(fm.hasSubstring("aabb"))
                    self.assertTrue(fm.hasSubstring("aaba"))
                    l, r = fm.range("a")
                    self.assertEqual(1, l)
                    self.assertEqual(5, r)
                    l, r = fm.range("b")
                    self.assertEqual(5, l)
                    self.assertEqual(7, r)
                    l, r = fm.range("ba")
                    self.assertEqual(5, l)
                    self.assertEqual(7, r)
                    l, r = fm.range("baaba")
                    self.assertEqual(6, l)
                    self.assertEqual(7, r)
                    self.assertTrue(fm.hasSubstring("abaaba"))
                    self.assertTrue(fm.hasSubstring("baaba"))
                    self.assertTrue(fm.hasSubstring("aaba"))
                    self.assertTrue(fm.hasSubstring("abaab"))
                    self.assertTrue(fm.hasSubstring("abaa"))
                    self.assertFalse(fm.hasSubstring("abc"))
                    self.assertFalse(fm.hasSubstring("abaabaa"))
                    self.assertFalse(fm.hasSubstring("ababa"))
                    self.assertFalse(fm.hasSubstring("z"))
                    self.assertFalse(fm.hasSubstring("zzzzzz"))
                    self.assertTrue(fm.hasSuffix("aba"))
                    self.assertTrue(fm.hasSuffix("ba"))
                    self.assertTrue(fm.hasSuffix("a"))
            
            def test_search_2(self):
                for fm in constructions("acgtacgtacgtacgt"):
                    self.assertFalse(fm.hasSubstring("aa"))
                    self.assertFalse(fm.hasSubstring("zz"))
                    self.assertFalse(fm.hasSuffix("ab"))
                    self.assertTrue(fm.hasSuffix("acgt"))
            
            def test_search_3(self):
                p, t = "ACGT", "ACGT"
                for fm in constructions(t):
                    matches = sorted(fm.occurrences(p))
                    self.assertEqual(1, len(matches))
                    self.assertEqual(0, matches[0])
                    self.assertEqual(matches, naive(p, t))
            
            def test_search_4(self):
                p, t = "AAA", "AAAAAA"
                for fm in constructions(t):
                    matches = sorted(fm.occurrences(p))
                    self.assertEqual(4, len(matches))
                    for i in xrange(0, 4):
                        self.assertEqual(i, matches[i])
                    self.assertEqual(matches, naive(p, t))
            
            def test_search_5(self):
                p, t = "ATAGCGGCG", "GTTATAGCTGATCGCGGCGATAGCGGCGAA"
                fm = FmIndex(t)
                for fm in constructions(t):
                    matches = sorted(fm.occurrences(p))
                    self.assertEqual(1, len(matches))
                    self.assertEqual(19, matches[0])
                    self.assertEqual(matches, naive(p, t))
            
            def test_search_random_1(self, num=10):
                import random
                for j in xrange(0, num):
                    alph = [ 'A', 'C', 'G', 'T' ]
                    # Generate random p
                    p = ''.join([ random.choice(alph) for i in xrange(0, 15) ])
                    # Generate random background for t
                    t = ''.join([ random.choice(alph) for i in xrange(0, 10900) ])
                    # Insert p in t 10 times
                    for i in xrange(0, 10):
                        ri = random.randint(0, len(t))
                        t = t[:ri] + p + t[ri:]
                    fm = FmIndex.fromString(t)
                    matches = sorted(fm.occurrences(p))
                    self.assertTrue(len(matches) >= 1)
                    nmatches = naive(p, t)
                    if matches != nmatches:
                        print "T:%s\nP:%s" % (t, p)
                    self.assertEqual(matches, nmatches)
        
        unittest.main(argv=[sys.argv[0]])
    
    else:
        t = args.text
        if t is None:
            if args.text_file is None:
                raise RuntimeError("Must specify --text or --text-file")
            th = open(args.text_file, 'r')
            t = th.read()
            th.close()
        if args.text_ignore_ws: t = ''.join(t.split())
        if args.text_uppercase: t = t.upper()
        import datetime
        stree = SuffixTree(t)
        for node in stree.nodes:
            assert node.repOk(t + '$')
        if args.dot is not None:
            with open(args.dot + ".dot", 'w') as dotOfh:
                stree.toDot(dotOfh, strs=args.string_lab)
            os.system("dot -Tpdf %s > %s" % (args.dot + ".dot", args.dot))
        print >>sys.stderr, "Suffix tree has %s nodes" % len(stree.nodes)
