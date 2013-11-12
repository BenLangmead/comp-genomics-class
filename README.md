Computational Genomics
======================

Code and examples for JHU Computational Genomics class.  Please feel free to submit [issues].

[issues]: https://github.com/BenLangmead/comp-genomics-class/issues

Notebooks
---------

The `notebooks` subdirectory contains the raw JSON for the iPython notebooks referenced in class.  The notebooks are also available as public GitHub gists and you can view readable versions of them at the following URLs:

* Exact and approximate matching
    * [Strings]
    * [Naive exact matching]
    * [Boyer-Moore]
    * [Inverted indexing 1]
    * [Inverted indexing 2]
    * [Inverted indexing 3]
    * [Naive approximate matching]
* Suffix indexes
    * [Trie map]
    * [Suffix trie]
    * [Suffix tree]
    * [Python binary search]
    * [Suffix array binary search]
    * [LCPs]
    * [Suffix array and LCPs from Suffix tree]
    * [Burrows-Wheeler Transform]
    * [Reversing BWT]
* Pairwise sequence alignment
    * [Edit distance]
    * [Global alignment]
    * [Local alignment]
    * [k-edit dynamic programming]
    * [String neighborhoods]
* Sequence assembly
    * [Suffix-prefix matches]
    * [De Bruijn graph]
    * [Error correction]
* Sequence classification
    * [Markov chains]

[Strings]: http://nbviewer.ipython.org/6512698
[Naive exact matching]: http://nbviewer.ipython.org/6513059
[Inverted indexing 1]: http://nbviewer.ipython.org/6582444
[Inverted indexing 2]: http://nbviewer.ipython.org/6584538
[Inverted indexing 3]: http://nbviewer.ipython.org/6582836
[Naive approximate matching]: http://nbviewer.ipython.org/6603391
[Boyer-Moore]: http://nbviewer.ipython.org/6603340
[Trie map]: http://nbviewer.ipython.org/6603619
[Suffix trie]: http://nbviewer.ipython.org/6603756
[Suffix tree]: http://nbviewer.ipython.org/6665861
[Python binary search]: http://nbviewer.ipython.org/6603756
[Suffix array binary search]: http://nbviewer.ipython.org/6765182
[LCPs]: http://nbviewer.ipython.org/6783863
[Suffix array and LCPs from Suffix tree]: http://nbviewer.ipython.org/6796858
[Burrows-Wheeler Transform]: http://nbviewer.ipython.org/6798379
[Reversing BWT]: http://nbviewer.ipython.org/6860491
[Edit distance]: http://nbviewer.ipython.org/6894694
[Global alignment]: http://nbviewer.ipython.org/6895625
[Local alignment]: http://nbviewer.ipython.org/6994170
[k-edit dynamic programming]: http://nbviewer.ipython.org/7011945
[String neighborhoods]: http://nbviewer.ipython.org/7012233
[Suffix-prefix matches]: http://nbviewer.ipython.org/7089885
[De Bruijn graph]: http://nbviewer.ipython.org/7237207
[Error correction]: http://nbviewer.ipython.org/7339417
[Markov chains]: http://nbviewer.ipython.org/7413873

These are for teaching purposes.  They are certainly not meant to be efficient.  Please feel free to submit [issues].

Other class resources
---------------------

If you are taking my class and you have any trouble accessing these resources, please contact me and I can help.  All of these articles should be easily accessible from the JHU campus or via VPN.

* Class readings
    * [Life and its Molecules](http://www.aaai.org/ojs/index.php/aimagazine/article/view/1744) by Lawrence Hunter
    * [A decade's perspective on DNA sequencing technology](http://www.nature.com/nature/journal/v470/n7333/full/nature09796.html) by Elaine Mardis
    * [Sequencing technologies -- the next generation](http://www.nature.com/nrg/journal/v11/n1/full/nrg2626.html)
    * [Suffix arrays: a new method for on-line string searches](http://dl.acm.org/citation.cfm?id=320218)
    * [Introduction to the Burrows-Wheeler Transform and FM Index](http://www.cs.jhu.edu/~langmea/resources/bwt_fm.pdf)
    * [Assembly of large genomes using second-generation sequencing](http://genome.cshlp.org/content/20/9/1165.long)
    * [How to apply de Bruijn graphs to genome assembly](http://www.nature.com/nbt/journal/v29/n11/full/nbt.2023.html)
    * [Computational prediction of eukaryotic protein-coding genes](http://www.nature.com/nrg/journal/v3/n9/execsumm/nrg890.html)
* Further reading
    * [Replacing suffix trees with enhanced suffix arrays](http://www.sciencedirect.com/science/article/pii/S1570866703000650)
    * [A Block-sorting Lossless Data Compression Algorithm](http://www.cs.jhu.edu/~langmea/resources/burrows_wheeler.pdf) (describes Burrows-Wheeler Transform)
    * [Opportunistic data structures with applications](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=892127) (describes FM Index)
    * [Ultrafast and memory-efficient alignment of short DNA sequences to the human genome](http://www.cs.jhu.edu/~langmea/resources/bowtie.pdf) (describes [Bowtie])
    * [Fast and accurate short read alignment with Burrows–Wheeler transform](http://bioinformatics.oxfordjournals.org/content/25/14/1754.long)
* Videos
    * Animation of [DNA wrapping and replication](http://www.youtube.com/watch?v=bW5JnYZImJA)
    * Animation of [Transcription and translation](http://www.youtube.com/watch?v=41_Ne5mS2ls)
    * PBS Documentary "DNA" (getting old, but still very good)
        * Part 1 of 5: [The Secret of Life](http://www.youtube.com/watch?v=d7ET4bbkTm0)
        * Part 3 of 5: [The Human Race](http://www.youtube.com/watch?v=kpoziqXldJM)
    * Animation of [how one "3rd-generation" sequencer works](http://www.youtube.com/watch?v=NHCJ8PtYCFc)
    * Many cool animations of [biological phenomena](http://www.johnkyrk.com/) by John Kyrk
    * Demo of [pairwise sequence alignment](http://www.cs.umd.edu/class/fall2011/cmsc423/demos/align.html)
    * Presentation describing [1st, 2nd and 3rd generation sequencing](http://www.youtube.com/watch?v=_ApDinCBt8g) (with campy music)
        * Note: Helicos is defunct, and Roche 454 and Life Tech SOLiD technologies are not very popular any more
* Recorded lectures
    * [Suffix tries and suffix trees](http://www.youtube.com/watch?v=hLsrPsFHPcQ)

[Bowtie]: http://bowtie-bio.sourceforge.net/index.shtml

TODO
----

* Add FM Index notebook
* Add co-traversal notebook

Contributors
------------

* [Ben Langmead]

[Ben Langmead]: http://www.cs.jhu.edu/~langmea/index.shtml
