A guide for students looking for datasets they can use for their final project.
Feel free to email me if you have a very specific need not addressed here.  When
you email me, please be as specific as possible about what sequences you're
looking for and why.

Also, please share anything new you learn with your classmates via Piazza.

Reference genomes
-----------------

You can download already-assembled "reference" genomes for many species,
including all of the most-studied "model" species.  I recommend [Ensembl]
as a good place to grab these.

[Ensembl]: http://useast.ensembl.org/index.html

Here are some shortcuts for some commonly used reference sequences:

* [Whole human Genome, GRCh37](ftp://ftp.ensembl.org/pub/release-73/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.73.dna.toplevel.fa.gz) (~ 3.1 billion nt)
* [Just human chromosome 22, GRCh37](ftp://ftp.ensembl.org/pub/release-73/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.73.dna.chromosome.22.fa.gz) (~ 50 million nt)
* [Whole mouse Genome, GRCm38](ftp://ftp.ensembl.org/pub/release-73/fasta/mus_musculus/dna/Mus_musculus.GRCm38.73.dna.toplevel.fa.gz) (~ 2.7 billion nt)
* [Just mouse chromosome 19, GRCm38](ftp://ftp.ensembl.org/pub/release-73/fasta/mus_musculus/dna/Mus_musculus.GRCm38.73.dna.chromosome.19.fa.gz) (~ 60 million nt)
* [Whole fruitfly Genome, BDGP5](ftp://ftp.ensembl.org/pub/release-73/fasta/drosophila_melanogaster/dna/Drosophila_melanogaster.BDGP5.73.dna.toplevel.fa.gz) (~170 million nt)
* [Whole roundworm Genome, WBcel235](ftp://ftp.ensembl.org/pub/release-73/fasta/caenorhabditis_elegans/dna/Caenorhabditis_elegans.WBcel235.73.dna.toplevel.fa.gz) (~100 million nt)
* [Whole yeast Genome, EF4](ftp://ftp.ensembl.org/pub/release-73/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.EF4.73.dna.toplevel.fa.gz) (~12 million nt)

Referenge genomes are long.
If you are working on a project that involves a non-trivial computation
over a reference genome (e.g. building an index or a large summary), you
might start with a small genome, or just a single chromosome of a larger
genome, then work your way up to longer strings.

Also, not that reference genomes, especially the longer ones, can contain
characters besides A, C, G and T.  Often, this will be an N.  These Ns
are placeholders; i.e. if there is a gap of known length between two
contigs, they may be "joined" with an appropriate-length stretch of Ns
between them.  Besides Ns, you may also see dashes (`-`) as well as other
[IUPAC nucleotide codes](http://www.bioinformatics.org/sms/iupac.html).

Sequencing reads
----------------

### Simulated versus real-world

Sometimes the most expediant way to get DNA sequences to test your software is to
generate them yourself.  E.g. if you would like some sequencing reads derived from
the fruitfly genome, you can download the whole fruitfly genome in compressed FASTA format, then run a very
simple piece of software to extract substrings from the genome.

### Software for simulating sequence reads

* [Mason](http://www.seqan.de/projects/mason/)
* [wgsim](https://github.com/lh3/wgsim)

### Where to get real-world reads

A good place to browse for real-world sequencing reads relevant to your project is the
[European Nucleotide Archive (ENA)](http://www.ebi.ac.uk/ena/).  Note that
most of the files there are big, so you might want to use tools like `curl`,
`gzip -dc` and `head` to avoid downloading entire files.

Output data from the [1000 Genomes Project] is hosted on [Simple Storage Service (S3)]
, part of [Amazon Web Services (AWS)].  See [this page](http://aws.amazon.com/1000genomes/).

[1000 Genomes Project]: http://www.1000genomes.org
[Simple Storage Service (S3)]: http://aws.amazon.com/s3/
[Amazon Web Services (AWS)]: http://aws.amazon.com

Protein sequences
-----------------

If your project involves aligning protein sequences to each other (e.g.
multiple alignment), alignment benchmark packages can be a good source
of example sequences.  Try:

* [PREFAB](http://www.drive5.com/muscle/prefab.htm) (see `in` and `ref` subdirectories of that archive)
