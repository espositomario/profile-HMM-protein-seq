# An HMM-based method to detect Kunitz domain starting from the BPTI structure
This repository contains the **bash script**, all the **pyhton codes**, and the intermediate and final results related to this study.
However, the following pipeline is designed to work for any other protein domain.

## Study workflow
The aim of this study is to develop an HMM-based method which reliably identifies the presence of the Kunitz domain in UniProtKB/SwissProt sequences. In principle, a profile HMM can be derived from unaligned sequences by training. However, the parameters for a profile HMM are more accurately estimated from a multiple sequence alignment (MSA) and this has become the method of choice (Bateman and Haft, 2002). The MSA was retrieved from the alignment of 77 structures similar to the BPTI. The HMM was trained over this MSA and then UniProtKB/SwissProt was adopted to optimize and test the classification performance of the method. 

## Requirements
The python code was tested on python 3.10 and pipeline on MacOS 13.


To run this pipeline the following programms need to be installed:

* CD-HIT 4.8.1
* blastpgp 2.2.26
* HMMER 3.3.2
```
conda create -n hmm_kunitz blast-legacy hmmer cd-hit 
conda activate hmm_kunitz 
```


Webtools links: 

* [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/)
* [Skyalign](http://skylign.org/) 
* [Uniprot ID Mapping](https://www.uniprot.org/id-mapping)

## 1. Training set selection
### BPTI as prototype and search for similar structures
The high-resolution structure of the bovine pancreatic trypsin inhibitor (1BPI) was chosen as the prototype of Kunitz domain to select the seeds (Parkin et al., 1996). The webtool [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/) was adopted to perform a pairwise structural alignment over the entire PDB (Krissinel and Henrick, 2005; Berman et al., 2000) . PDBeFold was run with default parameters and precision set to ‘highest’ and the results were selected by a Q-score > 0.75.

``` 
fasta_similar_structure='bpt1_result_qscore_0.75.fasta.seq' 
```

### Cluster identical sequences
To avoid a bias in the HMM construction, CD-HIT v4.8.1 was adopted to cluster identical sequences and select the longest representative for each cluster (Fu et al., 2012). A threshold of 100% identity was chosen to maintain also sequences differing for only one residue, so that no information on variation went lost.

```
cd-hit -i $fasta_similar_structure -o seeds_filt.fasta -c 1
```

## 2. MSA and HMM building
### Align structures and retrieve MSA
A multiple structure alignment between the 77 representativses structures was performed using the [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/). The MSA derived from the structure alignment, was downloaded and adopted as a training set for the HMM training.

extract pdb id with chain to align the structures on pdbefold

```
grep  '^>' seeds_filt.fasta | cut -d' ' -f1 | cut -c6- > sets/pdb_id_training.list
```

Align on [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/) and download the msa
```
msa='msa_seeds.seq'
grep . $msa > $msa.tmp && mv $msa.tmp $msa 
```
### Train the HMM 
The hmmbuild program provided by HMMER v3.3.2 was chosen to train the Kunitz’s HMM, leaving the optimal trimming on the MSA to the algorithm (Eddy, 2011). The HMM profile logo was plotted with [Skyalign](http://skylign.org/) (Wheeler et al., 2014).

```
hmmbuild kunitz.hmm $msa
````

## 3. Test set preparation
### Remove high-similarity sequences from the test-set
The entire UniProt/SwissProt release_2023_02 (SP) was chosen as a test set and the annotation of Kunitz domain (PF00014) according to PFAM v35.0 was chosen as reference to evaluate the classification performance. Before testing the model, the test set was elaborated in order to avoid a bias in the model evaluation. The seed sequences and all high similarity proteins (>95%), were removed from SP in order to perform a fair test of the HMM. To identify the high -similarity proteins, blastpgp v2.2.26 (gapped-BLAST) was run with default parameters, using the 77 training sequences as queries and the entire SP as target database (Altschul et al., 1997).







