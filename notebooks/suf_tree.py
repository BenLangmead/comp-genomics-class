#!/usr/bin/env python

"""
Suffix tree implementation using Ukkonen's algorithm.
"""

import sys
import os

class SuffixTree(object):
    
    class Node(object):
        """ Suffix tree node.  Contains offset, length of substring from T
            labeling the incoming edge.  Also contains outgoing edges, and some
            (hopefully O(1) space) extra annotations. """
        
        def __init__(self, off, ln, id=None):
            self.off = off    # offset into T of substring on edge leading into this node
            self.ln = ln      # length of substring on edge leading into this node
            self.slink = None # suffix link from this node
            self.id = id      # id; for leaf nodes, this is the suffix
            self.out = {}     # outgoing edges; characters x nodes
            self.extra = {}   # extra per-node info
        
        def isLeaf(self):
            return len(self.out) == 0
        
        def isRoot(self):
            return self.ln == 0
        
        def isInternal(self):
            return not self.isLeaf() and not self.isRoot()
    
    class Locus(object):
        """ A location in a suffix tree """
        
        def __init__(self, nodeAbove, nodeBelow, outChar, charsBelow):
            self.na = nodeAbove      # node above the locus
            self.nb = nodeBelow      # node below the locus
            self.oc = outChar        # char labeling edge we're on
            self.below = charsBelow  # # chars below the above-node we are
        
        def repOk(self):
            """ Make sure we're in a legitimate location """
            if self.below > 0:
                assert self.nb is not None
                assert self.oc is not None
                assert self.below < self.nb.ln
                assert self.nb is self.na.out[self.oc]
            else:
                assert self.nb is None
                assert self.oc is None
            return True
    
    def stripAnnotations(self):
        """ Strip away any extra information associated with nodes """
        for n in self.nodes: n.extra = {}
    
    def __splitEdge(self, node, outc, depth):
        """ Create a new node in the middle of the edge given by node, outc """
        assert depth > 0
        assert outc in node.out
        child = node.out[outc]
        assert depth < child.ln
        mid = self.Node(child.off, depth)
        self.nodes.append(mid)
        mid.extra['parent'] = node
        child.extra['parent'] = mid
        node.out[outc] = mid
        child.off += depth
        child.ln -= depth
        mid.out[self.s[child.off]] = child
        return mid
    
    def fromRoot(self, q):
        """ Walk down from the root, following a path corresponding to string
            q.  Return coordinates of where walk ended. """
        i = 0
        cur, s = self.root, self.s
        while i < len(q):
            c = q[i]
            if c not in cur.out:
                return None, None, None
            child = cur.out[c]
            assert c == s[child.off]
            i += 1
            j = 1
            while j < child.ln and i < len(q):
                if q[i] != s[child.off + j]:
                    return None, None, None
                j += 1 # advance text pointer
                i += 1 # advance query pointer
            if j == child.ln:
                cur = child # exhausted edge
            else:
                assert i == len(q)
                return (cur, c, j) # exhausted query string in middle of edge
        return (cur, None, 0) # exhausted query string at internal node
    
    def __skipCount(self, v, d, off):
        """ Given a node and a substring of T...
            Returns a node, character and depth.  The node is the node above the  """
        if not v.isRoot() and v.slink is None:
            off = v.off
            d += v.ln
            v = v.extra['parent']
            assert v.isRoot() or v.slink is not None
        if v.isRoot():
            # Handle case where parent is root
            assert d > 0
            d -= 1
            off += 1
            if d > 0:
                node, c, depth = self.fromRoot(self.s[off:off+d])
                assert node is None or depth == 0 or depth < node.out[c].ln
                return node, c, depth
            else:
                return v, None, 0
        else:
            # Handle case where parent is internal node
            assert v.slink is not None
            sv = cur = v.slink
            assert not sv.isLeaf()
            if d == 0:
                return sv, None, 0
            assert off is not None
            i = off
            while d > 0:
                c = self.s[i]
                next = cur.out[c]
                if next.ln < d:
                    d -= next.ln
                    i += next.ln
                    cur = next
                elif next.ln == d:
                    return next, None, 0
                else:
                    assert d < cur.out[c].ln
                    return cur, c, d
            assert False
    
    def __ukkonen(self, root, bottom, toDot=None, sanity=False):
        """ Perform all phases and extensions of Ukkonen's algorithm """
        s = self.s
        # Some extension positions are "rooted", i.e. all subsequent
        # extensions of that suffix will fall into "Case 1" whereby the root
        # edge length is incremented by 1
        skipext = 1
        lastleaf = bottom
        for i in xrange(0, len(s)-1): # Phases
            lastInternal = None
            c = s[i+1] # new character
            lastn, lastdepth, lastoff = lastleaf.extra['parent'], i + 1 - lastleaf.off, lastleaf.off
            for j in xrange(skipext, i+2): # Extensions
                node, outc, depth = self.__skipCount(lastn, lastdepth, lastoff)
                assert node is not None
                if depth == 0: # skip-count ended in node
                    if lastInternal is not None:
                        assert lastInternal.slink is None
                        lastInternal.slink = node
                        lastInternal = None
                    if c not in node.out:
                        # Rule 2: not already there; create a new leaf
                        lastn, lastdepth, lastoff = node, 0, i+1
                        node.out[c] = lastleaf = self.Node(i+1, len(s)-i-1, id=j)
                        self.nodes.append(lastleaf)
                        node.out[c].extra['parent'] = node
                    else: break # Rule 3: Already there
                else: # skip-count ended in edge
                    assert outc is not None
                    child = node.out[outc]
                    if s[child.off + depth] != c:
                        # Rule 2: Not already there; split edge
                        mid = lastn = self.__splitEdge(node, outc, depth)
                        lastdepth, lastoff = 0, i+1
                        # mid is a new internal node, in need of a suffix link 
                        mid.out[c] = lastleaf = self.Node(i+1, len(s)-i-1, id=j)
                        self.nodes.append(lastleaf)
                        mid.out[c].extra['parent'] = mid
                        if lastInternal is not None:
                            assert lastInternal.slink is None
                            lastInternal.slink = mid
                        lastInternal = mid
                    else:
                        assert lastInternal is None
                        break # Rule 3: Already there
                skipext = max(skipext, j+1)
            assert lastInternal is None
            if toDot is not None:
                fn = "%s.phase%d.dot" % (toDot, i)
                with open(fn, 'w') as ost:
                    self.toDot(ost, strs=True)
            if sanity:
                for j in xrange(0, i+2):
                    self.fromRoot(s[j:i+2])
        self.stripAnnotations()
        if sanity:
            assert self.repOk()
    
    def __init__(self, s, toDot=None, sanity=False):
        """ Ukkonen's algorithm to build suffix tree """
        s += '$'
        self.s = s
        self.root = root = self.Node(0, 0)
        root.extra['parent'] = None
        root.out[s[0]] = bottom = self.Node(0, len(s), id=0)
        bottom.extra['parent'] = root
        assert bottom.isLeaf()
        self.nodes = [root, bottom]
        self.__ukkonen(root, bottom, toDot=toDot, sanity=sanity)
    
    def suffixesBelow(self, l):
        """ Given a suffix tree locus, return a list of the suffixes below this
            point in the tree. """
        sufs = []
        assert l.repOk()
        # If we're not at a node...
        if l.below > 0:
            # ...descend to the next node below
            l = self.Locus(l.nb, None, None, 0)
        def __suffixesBelowHelper(n, sufs):
            if n.isLeaf(): sufs.append(n.id)
            for child in n.out.itervalues():
                __suffixesBelowHelper(child, sufs)
        __suffixesBelowHelper(l.na, sufs)
        return sufs
    
    def mems(self, p, l=4):
        """ Find maximal exact matches (MEMs) between t and the given pattern
            p.  Only report MEMs that are at least l characters long. """
        s = self.s
        node, child = self.root, None
        below, depth = 0, 0
        c = ''
        mems = []
        depths = []
        for i in xrange(0, len(p)):
            cp = p[i]
            # How do we know when we've reached the end of a MEM?  Basically,
            # whenever we set of suffixes below the current pointer changes.
            first = True
            assert depth <= i
            while True:
                if below == 0:
                    assert child is None
                    if cp in node.out:
                        if first and depth >= l:
                            # Gather suffixes below the other children, besides
                            # the one we're investigating
                            for ic, ichild in node.out.iteritems():
                                if ic == cp: continue
                                for suf in self.suffixesBelow(self.Locus(ichild, None, None, 0)):
                                    mems.append((suf, i-depth, depth))
                        below += 1
                        depth += 1
                        child = node.out[cp] # follow outgoing edge
                        if below == child.ln:
                            node, child, below = child, None, 0
                        break
                    else:
                        # No outgoing edge on next pattern character
                        if first and depth >= l:
                            # Gather suffixes below
                            for suf in self.suffixesBelow(self.Locus(node, None, None, 0)):
                                mems.append((suf, i-depth, depth))
                        node, c, below = self.__skipCount(node, below, None)
                        depth -= 1
                        if below > 0:
                            child = node.out[c]
                            assert below < child.ln
                        else:
                            child = None
                else:
                    assert child is not None
                    assert below < child.ln, "below=%d, child.ln=%d" % (below, child.ln) # follow edge we're already on
                    assert below > 0
                    if s[child.off + below] != cp:
                        if first and depth >= l:
                            # Gather suffixes below
                            for suf in self.suffixesBelow(self.Locus(child, None, None, 0)):
                                mems.append((suf, i-depth, depth))
                        assert node.slink is not None
                        node, c, below = self.__skipCount(node, below, child.off)
                        depth -= 1
                        if below > 0:
                            child = node.out[c]
                            assert below < child.ln
                        else:
                            child = None
                    else:
                        below += 1
                        depth += 1
                        if below == child.ln:
                            node, child, below = child, None, 0
                        break
                first = False
            depths.append(depth)
        if depth >= l:
            # Gather suffixes below
            if below > 0:
                assert child is not None
                node = child
            for suf in self.suffixesBelow(self.Locus(node, None, None, 0)):
                mems.append((suf, len(p) - depth, depth))
        return mems, depths
    
    def repOk(self):
        """ Check that tree adheres to definition of suffix tree """
        s = self.s
        nleaves = 0
        for n in self.nodes:
            if n.isLeaf():
                nleaves += 1
            elif n.isInternal():
                assert len(n.out) > 1
        assert nleaves == len(s)
        seen = set()
        for i in xrange(0, len(s)):
            node, c, depth = self.fromRoot(s[i:])
            assert node is not None
            assert node.isLeaf()
            seen.add(node)
        assert len(seen) == nleaves
        return True
    
    def hasSubstring(self, s):
        """ Return true iff s appears as a substring """
        node, c, off = self.fromRoot(s)
        return node is not None
    
    def hasSuffix(self, s):
        """ Return true iff s is a suffix """
        node, c, depth = self.fromRoot(s)
        if node is None:
            return False # fell off the tree
        if depth is 0:
            # finished on top of a node
            return '$' in node.out
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return self.s[node.out[c].off + depth]  == '$'
    
    def saAndLcp(self):
        """ Generate suffix array and an LCP array corresponding to this
            suffix tree.  For a given SA elt, the LCP returned is the LCP
            between the elt and the next-smallest.  For the first suffix, LCP
            of 0 is reported. """
        self.minSinceLeaf = 0
        def __visit(n, depth):
            if len(n.out) == 0:
                # leaf node, yield offset and LCP with previous
                yield (len(self.s) - depth, self.minSinceLeaf)
                # reset LCP to depth of most recently reported leaf
                self.minSinceLeaf = depth
            # visit children in lexicographical order
            for c, child in sorted(n.out.iteritems()):
                for x in __visit(child, depth + child.ln):
                    yield x
                # after each child visit, perhaps decrease
                # minimum-depth-since-last-leaf value
                self.minSinceLeaf = min(self.minSinceLeaf, depth)
        for x in __visit(self.root, 0):
            yield x
    
    def sa(self):
        """ Generate suffix array corresponding to this. """
        def __visit(n, depth):
            if len(n.out) == 0:
                # leaf node, yield offset and LCP with previous
                yield len(self.s) - depth
            # visit children in lexicographical order
            for c, child in sorted(n.out.iteritems()):
                for x in __visit(child, depth + child.ln):
                    yield x
        for x in __visit(self.root, 0):
            yield x
    
    def toDot(self, ost, strs=False, suflinks=True, labelNonLeaves=False):
        """ Write dot version of suffix tree to given output stream """
        ost.write("digraph \"Suffix tree\" {\n")
        ost.write("  node [shape=circle] ;\n")
        ost.write('  edge [fontname = "helvetica"] ;\n')
        n2id = {}
        for i in xrange(0, len(self.nodes)):
            n2id[self.nodes[i]] = i
        for n in self.nodes:
            if n.isLeaf():
                ost.write("  n%d [label=\"%d\" shape=square] ;\n" % (n2id[n], n.id))
            else:
                ost.write("  n%d [label=\"%s\" ] ;\n" % (n2id[n], str(n2id[n]) if labelNonLeaves else ""))
            for c, child in n.out.iteritems():
                childId = n2id[child]
                if strs:
                    lab = self.s[child.off:(child.off + child.ln)]
                else:
                    lab = "%d, %d" % (child.off, child.ln)
                ost.write("  n%d -> n%d [label=\"%s\"] ;\n" % (n2id[n], childId, lab))
            if suflinks and n.slink is not None:
                svId = n2id[n.slink]
                ost.write("  n%d -> n%d [constraint=false style=dotted] ;\n" % (n2id[n], svId))
        ost.write("}\n")

def naiveMEMs(p, t, l=4):
    mems = []
    # slide p along t
    for i in xrange(l-len(p), len(t)-l+1):
        j = 0
        # look for strings of matches
        if i+j < 0:
            j -= (i+j)
        while j < len(p) and i+j >= 0 and i+j < len(t):
            if p[j] == t[i+j]:
                origj = j
                ln = 1
                j += 1
                while j < len(p) and i+j < len(t) and p[j] == t[i+j]:
                    ln += 1
                    j += 1
                if ln >= l:
                    mems.append((i+origj, origj, ln))
            j += 1
    return sorted(mems)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test suffix tree functionality')
    
    parser.add_argument(\
        '--text', metavar='string', type=str, help='Text T')
    parser.add_argument(\
        '--dot', metavar='path', type=str, help='Write dot output to PDF file')
    parser.add_argument(\
        '--ukkonen-dot', metavar='path', type=str, help='Write Ukkonen phases dot output to PDF file with this prefix')
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
    parser.add_argument(\
        '--sanity', action='store_const', const=True, default=False, help='Do sanity checks')
    parser.add_argument(\
        '--label-leaves', action='store_const', const=True, default=False, help='Label leaves of suffix tree')
    parser.add_argument(\
        '--no-suffix-links', action='store_const', const=True, default=False, help='Don\'t write suffix links in dot output')
    
    args = parser.parse_args()
    
    if args.test:
        import sys
        import unittest
        
        class Test(unittest.TestCase):
            
            def test_build_1(self):
                s = "TACTAA"
                st = SuffixTree(s, sanity=True)
                self.assertTrue(st.hasSuffix(s))
            
            def test_build_random(self):
                import random
                random.seed(77)
                for i in xrange(6, 40, 2):
                    for trial in xrange(0, 20):
                        s = ''.join([random.choice("ACGT") for h in xrange(0, i)])
                        st = SuffixTree(s, sanity=True)
                        self.assertTrue(st.hasSuffix(s))
            
            def test_substring_1(self):
                st = SuffixTree("ACGT")
                self.assertTrue(st.hasSubstring("A"))
                self.assertTrue(st.hasSubstring("AC"))
                self.assertTrue(st.hasSubstring("ACG"))
                self.assertTrue(st.hasSubstring("ACGT"))
                self.assertFalse(st.hasSubstring("D"))
                self.assertFalse(st.hasSubstring("ACGTACGT"))
            
            def test_suffix_1(self):
                st = SuffixTree("ACGT")
                self.assertFalse(st.hasSuffix("A"))
                self.assertFalse(st.hasSuffix("AC"))
                self.assertFalse(st.hasSuffix("ACG"))
                self.assertTrue(st.hasSuffix("ACGT"))
                self.assertFalse(st.hasSuffix("D"))
                self.assertFalse(st.hasSuffix("ACGTACGT"))
                self.assertTrue(st.hasSuffix("CGT"))
                self.assertTrue(st.hasSuffix("GT"))
                self.assertTrue(st.hasSuffix("T"))
                self.assertTrue(st.hasSuffix(""))
            
            def test_suffix_2(self):
                t = "abaaba"
                st = SuffixTree(t)
                for i in xrange(0, len(t)+1):
                    self.assertTrue(st.hasSuffix(t[i:]))
                self.assertFalse(st.hasSuffix("abaa"))
            
            def test_sa_1(self):
                t = "abaaba"
                st = SuffixTree(t)
                esa = [ x for x in st.sa() ]
                self.assertEqual([6, 5, 2, 3, 0, 4, 1], esa)
            
            def test_salcp_1(self):
                t = "abaaba"
                st = SuffixTree(t)
                esa = [ x for x in st.saAndLcp() ]
                self.assertEqual(6, esa[0][0])
                self.assertEqual(5, esa[1][0])
                self.assertEqual(2, esa[2][0])
                self.assertEqual(3, esa[3][0])
                self.assertEqual(0, esa[4][0])
                self.assertEqual(4, esa[5][0])
                self.assertEqual(1, esa[6][0])
                
                self.assertEqual(0, esa[0][1])
                self.assertEqual(0, esa[1][1])
                self.assertEqual(1, esa[2][1])
                self.assertEqual(1, esa[3][1])
                self.assertEqual(3, esa[4][1])
                self.assertEqual(0, esa[5][1])
                self.assertEqual(2, esa[6][1])
            
            def test_mems_1(self):
                t, p = "abaaba", "aba"
                st = SuffixTree(t)
                mems, depths = st.mems(p, 4)
                self.assertEqual([], mems)
                self.assertEqual([1, 2, 3], depths)
            
            def test_mems_2(self):
                t, p = "abaaba", "abababa"
                st = SuffixTree(t)
                mems, depths = st.mems(p, 4)
                self.assertEqual([], mems)
                self.assertEqual(sorted(mems), naiveMEMs(p, t, 4))
                self.assertEqual([1, 2, 3, 2, 3, 2, 3], depths)
            
            def test_mems_3(self):
                t, p = "abaaba", "abababa"
                st = SuffixTree(t)
                mems, _ = st.mems(p, 3)
                self.assertEqual([(0, 0, 3), (3, 0, 3), (0, 2, 3), (3, 2, 3), (0, 4, 3), (3, 4, 3)], mems)
                self.assertEqual(sorted(mems), naiveMEMs(p, t, 3))
            
            def test_mems_random1(self):
                import random
                random.seed(773)
                for trial in xrange(0, 20):
                    t = ''.join([random.choice("ACGT") for h in xrange(0, 100)])
                    p = ''.join([random.choice("ACGT") for h in xrange(0, 10)])
                    st = SuffixTree(t, sanity=True)
                    mems, _ = st.mems(p, 5)
                    self.assertEqual(sorted(mems), naiveMEMs(p, t, 5))
        
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
        stree = SuffixTree(t, toDot=args.ukkonen_dot, sanity=args.sanity)
        assert stree.repOk()
        if args.dot is not None:
            with open(args.dot + ".dot", 'w') as dotOfh:
                stree.toDot(dotOfh, strs=args.string_lab, suflinks=not args.no_suffix_links)
            os.system("dot -Tpdf %s > %s" % (args.dot + ".dot", args.dot))
        print >>sys.stderr, "Suffix tree has %s nodes" % len(stree.nodes)
