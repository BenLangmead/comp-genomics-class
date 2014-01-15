Computational Genomics
======================

Code and examples for JHU Computational Genomics class.  Please feel free to submit [issues].

[issues]: https://github.com/BenLangmead/comp-genomics-class/issues

Notebooks
---------

The `notebooks` subdirectory contains the raw JSON for the iPython notebooks referenced in class.  The notebooks are also available as public GitHub gists and you can view readable versions of them at the following URLs:

* Exact and approximate matching
    * [Strings](http://nbviewer.ipython.org/6512698)
    * [Naive exact matching](http://nbviewer.ipython.org/8258880)
    * [Z algorithm (fundamental preprocessing)](http://nbviewer.ipython.org/7473392)
    * [Inverted indexing 1](http://nbviewer.ipython.org/6582444)
    * [Inverted indexing 2](http://nbviewer.ipython.org/6584538)
    * [Inverted indexing 3](http://nbviewer.ipython.org/6582836)
    * [Naive approximate matching](http://nbviewer.ipython.org/6603391)
    * [Index-assisted Boyer-Moore](http://nbviewer.ipython.org/6603340)
* Suffix indexes
    * [Trie map](http://nbviewer.ipython.org/6603619)
    * [Suffix trie](http://nbviewer.ipython.org/6603756)
    * [Suffix tree](http://nbviewer.ipython.org/6665861)
    * [Python binary search](http://nbviewer.ipython.org/6603756)
    * [Suffix array binary search](http://nbviewer.ipython.org/6765182)
    * [Longest common prefix (LCP)](http://nbviewer.ipython.org/6783863)
    * [Suffix array and LCPs from Suffix tree](http://nbviewer.ipython.org/6796858)
    * [Burrows-Wheeler Transform](http://nbviewer.ipython.org/6798379)
    * [Reversing BWT](http://nbviewer.ipython.org/6860491)
    * [FM Index](http://nbviewer.ipython.org/7437031)
* Pairwise sequence alignment
    * [Edit distance](http://nbviewer.ipython.org/6894694)
    * [Global alignment](http://nbviewer.ipython.org/6895625)
    * [Longest common subsequence (LCS)](http://nbviewer.ipython.org/7452174)
    * [k-edit alignment (approximate matching)](http://nbviewer.ipython.org/7452696)
    * [Local alignment](http://nbviewer.ipython.org/6994170)
    * [Index-assisted k-edit dynamic programming](http://nbviewer.ipython.org/7011945)
    * [String neighborhoods](http://nbviewer.ipython.org/7012233)
    * [Co-traversal](http://nbviewer.ipython.org/7438200)
* Sequence assembly
    * [Suffix-prefix matches](http://nbviewer.ipython.org/7089885)
    * [De Bruijn graph](http://nbviewer.ipython.org/7237207)
    * [Error correction](http://nbviewer.ipython.org/7339417)
* Sequence classification
    * [Markov chain](http://nbviewer.ipython.org/7413873)
    * [Higher order Markov chain](http://nbviewer.ipython.org/7468937)
    * [Hidden Markov Model (HMM)](http://nbviewer.ipython.org/7460513)
* File formats
    * [FASTA](http://nbviewer.ipython.org/gist/BenLangmead/8307011)
    * [FASTQ](http://nbviewer.ipython.org/gist/BenLangmead/8376306)

These are for teaching purposes.  They are certainly not meant to be efficient.  Please feel free to submit [issues].

Other class resources
---------------------

If you are taking my class and you have any trouble accessing these resources, please contact me and I can help.  All of these articles should be easily accessible from the JHU campus or via [VPN](http://portalcontent.johnshopkins.edu/sslvpn/JHConnect-FAQ.html) / [library proxy](http://old.library.jhu.edu/services/computing/proxyfaqs.html).

* Class readings (see syllabus for where these fit in)
    * [Life and its Molecules](http://www.aaai.org/ojs/index.php/aimagazine/article/view/1744) by Lawrence Hunter
    * [A decade's perspective on DNA sequencing technology](http://www.nature.com/nature/journal/v470/n7333/full/nature09796.html) by Elaine Mardis
    * [Sequencing technologies -- the next generation](http://www.nature.com/nrg/journal/v11/n1/full/nrg2626.html) by Michael Metzker
    * [The DNA Data Deluge](http://spectrum.ieee.org/biomedical/devices/the-dna-data-deluge) by Mike Schatz and Ben Langmead
    * [Suffix arrays: a new method for on-line string searches](http://dl.acm.org/citation.cfm?id=320218) by Udi Manber and Gene Myers
    * [Introduction to the Burrows-Wheeler Transform and FM Index](http://www.cs.jhu.edu/~langmea/resources/bwt_fm.pdf) by Langmead
    * [Assembly of large genomes using second-generation sequencing](http://genome.cshlp.org/content/20/9/1165.long) by Mike Schatz et al
    * [How to apply de Bruijn graphs to genome assembly](http://www.nature.com/nbt/journal/v29/n11/full/nbt.2023.html) by Phillip Compeau et al
    * [Computational prediction of eukaryotic protein-coding genes](http://www.nature.com/nrg/journal/v3/n9/execsumm/nrg890.html) by Michael Zhang
* Further reading
    * [Replacing suffix trees with enhanced suffix arrays](http://www.sciencedirect.com/science/article/pii/S1570866703000650) by Mohamed Abouelhoda et al
    * [A Block-sorting Lossless Data Compression Algorithm](http://www.cs.jhu.edu/~langmea/resources/burrows_wheeler.pdf) by Michael Burrows and David Wheeler (describes Burrows-Wheeler Transform)
    * [Opportunistic data structures with applications](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=892127) by Paolo Ferragina and Giovanni Manzini (describes FM Index)
    * [Ultrafast and memory-efficient alignment of short DNA sequences to the human genome](http://www.cs.jhu.edu/~langmea/resources/bowtie.pdf) by Langmead et al (describes [Bowtie])
    * [Fast and accurate short read alignment with Burrows–Wheeler transform](http://bioinformatics.oxfordjournals.org/content/25/14/1754.long) by Heng Li and Richard Durbin (describes [BWA])
* Videos
    * Animation of [DNA wrapping and replication](http://www.youtube.com/watch?v=bW5JnYZImJA)
    * Animation of [Transcription and translation](http://www.youtube.com/watch?v=41_Ne5mS2ls)
    * PBS Documentary "DNA" (getting old, but still very good)
        * Part 1 of 5: [The Secret of Life](http://www.youtube.com/watch?v=d7ET4bbkTm0)
        * Part 3 of 5: [The Human Race](http://www.youtube.com/watch?v=kpoziqXldJM)
    * Video describing how Illumina's [sequencing-by-synthesis](http://www.youtube.com/watch?v=l99aKKHcxC4) technology works
    * Animation of [how one "3rd-generation" sequencer works](http://www.youtube.com/watch?v=NHCJ8PtYCFc)
    * Many cool animations of [biological phenomena](http://www.johnkyrk.com/) by John Kyrk
    * Demo of [pairwise sequence alignment](http://www.cs.umd.edu/class/fall2011/cmsc423/demos/align.html)
    * Presentation describing [1st, 2nd and 3rd generation sequencing](http://www.youtube.com/watch?v=_ApDinCBt8g) (with campy music)
        * Note: Helicos is defunct, and Roche 454 and Life Tech SOLiD technologies are not very popular any more
* Notebooks
    * [Traveling Salesman Problem](http://nbviewer.ipython.org/url/norvig.com/ipython/TSPv3.ipynb) by Peter Norvig
    * [Write a Genome Assembler](http://nbviewer.ipython.org/urls/raw.github.com/cschin/Write_A_Genome_Assembler_With_IPython/master/Write_An_Assembler.ipynb) by Jason Chin
* Textbooks and lecture notes for other classes
    * [Algorithms](http://www.cs.berkeley.edu/~vazirani/algorithms/) by Vazirani et al
        * Check out the first two chapters if you need some analysis review, and check out the chapter on [dynamic programming](http://www.cs.berkeley.edu/~vazirani/algorithms/chap6.pdf).
* Recorded lectures for this class
    * [Suffix tries and suffix trees](http://www.youtube.com/watch?v=hLsrPsFHPcQ)

[Bowtie]: http://bowtie-bio.sourceforge.net/index.shtml
[BWA]: http://bio-bwa.sourceforge.net

Possible notebook additions
---------------------------

* Boyer-Moore
* Higher-order HMM
* Spliced alignment
* Minimum path cover on DAG to recover isoforms
* Pair HMMs
* Profile HMMs

Contributors
------------

* [Ben Langmead]

[Ben Langmead]: http://www.cs.jhu.edu/~langmea/index.shtml
