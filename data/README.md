A guide for students looking for datasets they can use for their final project.

Reference genomes
=================

Already-assembled genomes for various species.  I recommend [UCSC] as the place to grab these.

[UCSC]: http://hgdownload.soe.ucsc.edu/downloads.html

Here are some shortcuts for some commonly used reference sequences:

* [Whole human Genome, GRCh37](ftp://ftp.ensembl.org/pub/release-73/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.73.dna.toplevel.fa.gz)
* [Just human chromosome 22, GRCh37](ftp://ftp.ensembl.org/pub/release-73/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.73.dna.chromosome.22.fa.gz)
* [Whole mouse Genome, GRCm38](ftp://ftp.ensembl.org/pub/release-73/fasta/mus_musculus/dna/Mus_musculus.GRCm38.73.dna.toplevel.fa.gz)
* [Just mouse chromosome 19, GRCm38](ftp://ftp.ensembl.org/pub/release-73/fasta/mus_musculus/dna/Mus_musculus.GRCm38.73.dna.chromosome.19.fa.gz)
* [Whole fruitfly Genome, BDGP5](ftp://ftp.ensembl.org/pub/release-73/fasta/drosophila_melanogaster/dna/Drosophila_melanogaster.BDGP5.73.dna.toplevel.fa.gz)
* [Whole roundworm Genome, WBcel235](ftp://ftp.ensembl.org/pub/release-73/fasta/caenorhabditis_elegans/dna/Caenorhabditis_elegans.WBcel235.73.dna.toplevel.fa.gz)
* [Whole yeast Genome, EF4](ftp://ftp.ensembl.org/pub/release-73/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.EF4.73.dna.toplevel.fa.gz)

Sequencing reads
================

Simulated versus real-world
---------------------------

Sometimes the most expediant way to get DNA sequences to test your software is to
generate them yourself.  E.g. if you would like some sequencing reads derived from
the fruitfly genome, you can download the whole fruitfly genome in compressed FASTA format, then run a very
simple piece of software to extract substrings from the genome.

Software for simulating sequence reads
--------------------------------------

* [Mason](http://www.seqan.de/projects/mason/)
* [wgsim](https://github.com/lh3/wgsim)

Where to get real-world data
----------------------------

A good place to browse for real-world sequencing reads relevant to your project is the
[European Nucleotide Archive (ENA)](http://www.ebi.ac.uk/ena/).  Note that
most of the files there are big, so you might want to use tools like `curl`,
`gzip -dc` and `head` to avoid downloading entire files.
