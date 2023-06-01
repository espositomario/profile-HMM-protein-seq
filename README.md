# An HMM-based method to detect Kunitz domain starting from the BPTI structure
This repository contains the **bash commands**, all the **pyhton codes**, and the intermediate and final results of this [project](https://github.com/espositomario/HMM_Kunitz/blob/e762b5ff539bf6a3f77e75765ed467a57e95d42f/Mario%20Esposito%20-%20LB1%20project%20report.pdf) related to the course of Laboratory of Bioinformatics 1 of the MSc in Bioinformatics - University of Bologna.

Altough this pipeline was designed specifically to model the Kunitz domain it was supposed to work for any protein domain.

## Table of contents

* [Requirements](https://github.com/espositomario/HMM_Kunitz#requirements)
* [0. Study Workflow](https://github.com/espositomario/HMM_Kunitz#study-workflow)
* [1. Training set selection](https://github.com/espositomario/HMM_Kunitz#1-training-set-selection)
	* [1.1. BPTI as prototype and search for similar structures](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#11-bpti-as-prototype-and-search-for-similar-structures)
	* [1.2. Cluster identical sequences](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#12-cluster-identical-sequences)
* [2. MSA and HMM building](https://github.com/espositomario/HMM_Kunitz#2-msa-and-hmm-building)
	* [2.1 Align structures and retrieve MSA](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#21-align-structures-and-retrieve-msa)
	* [2.2 Train the HMM](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#22-train-the-hmm)
* [3. Test set preparation](https://github.com/espositomario/HMM_Kunitz#3-test-set-preparation)
	* [3.1 Remove high-similarity sequences from the test-set](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#31-remove-high-similarity-sequences-from-the-test-set)
	* [3.2 Test the model](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#32-test-the-model)
* [4. E-value optimization and classification benchmark](https://github.com/espositomario/HMM_Kunitz#4-e-value-optimization-and-classification-benchmark)
	* [4.1 Generate the two subsets by random spplitting Uniprot](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#41-generate-the-two-subsets-by-random-spplitting-uniprot)
	* [4.2 E-value optimization and classification benchmark](https://github.com/espositomario/HMM_Kunitz/blob/main/README.md#42-e-value-optimization-and-classification-benchmark)
* [References](https://github.com/espositomario/HMM_Kunitz#references)


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

## Study workflow
The aim of this study is to develop an HMM-based method which reliably identifies the presence of the Kunitz domain in UniProtKB/SwissProt sequences. In principle, a profile HMM can be derived from unaligned sequences by training. However, the parameters for a profile HMM are more accurately estimated from a multiple sequence alignment (MSA) and this has become the method of choice (Bateman and Haft, 2002). The MSA was retrieved from the alignment of 77 structures similar to the BPTI. The HMM was trained over this MSA and then UniProtKB/SwissProt was adopted to optimize and test the classification performance of the method. 


<img src="https://github.com/espositomario/HMM_Kunitz/assets/104198915/195174ab-7b28-4418-a0ed-2aad2de85ac5" alt="drawing" style="width:600px;"/>


## 1. Training set selection
### 1.1 BPTI as prototype and search for similar structures
The high-resolution structure of the bovine pancreatic trypsin inhibitor (1BPI) was chosen as the prototype of Kunitz domain to select the seeds (Parkin et al., 1996). The webtool [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/) was adopted to perform a pairwise structural alignment over the entire PDB (Krissinel and Henrick, 2005; Berman et al., 2000) . PDBeFold was run with default parameters and precision set to ‘highest’ and the results were selected by a Q-score > 0.75.

_#download fasta sequences_
``` 
fasta_similar_structure='bpt1_result_qscore_0.75.fasta.seq' 
```

### 1.2 Cluster identical sequences
To avoid a bias in the HMM construction, CD-HIT v4.8.1 was adopted to cluster identical sequences and select the longest representative for each cluster (Fu et al., 2012). A threshold of 100% identity was chosen to maintain also sequences differing for only one residue, so that no information on variation went lost.

```
cd-hit -i $fasta_similar_structure -o seeds_filt.fasta -c 1
```

## 2. MSA and HMM building
### 2.1 Align structures and retrieve MSA
A multiple structure alignment between the  representativses structures was performed using the [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/). The MSA derived from the structure alignment, was downloaded and adopted as a training set for the HMM training.

#_Extract pdb id with chain to align the structures on pdbefold_

```
grep  '^>' seeds_filt.fasta | cut -d' ' -f1 | cut -c6- > sets/pdb_id_training.list
```

_#Align on [PDBeFold](https://www.ebi.ac.uk/msd-srv/ssm/) and download the msa_
```
msa='msa_seeds.seq'
grep . $msa > $msa.tmp && mv $msa.tmp $msa 
```
### 2.2 Train the HMM 
The hmmbuild program provided by HMMER v3.3.2 was chosen to train the Kunitz’s HMM, leaving the optimal trimming on the MSA to the algorithm (Eddy, 2011). The HMM profile logo was plotted with [Skyalign](http://skylign.org/) (Wheeler et al., 2014).

```
hmmbuild kunitz.hmm $msa
````

## 3. Test set preparation
### 3.1 Remove high-similarity sequences from the test-set
The entire UniProt/SwissProt release_2023_02 (SP) was chosen as a test set and the annotation of Kunitz domain (PF00014) according to PFAM v35.0 was chosen as reference to evaluate the classification performance. Before testing the model, the test set was elaborated in order to avoid a bias in the model evaluation. The seed sequences and all high similarity proteins (>95%), were removed from SP in order to perform a fair test of the HMM. To identify the high-similarity proteins, blastpgp v2.2.26 (gapped-BLAST) was run with default parameters, using the training sequences as queries and the entire SP as target database (Altschul et al., 1997).

_#map the training sequences PDB IDs to UniProt IDs_
```
id_mapped='sets/id_mapped.list'
tail +2 $id_mapped | cut -f 2 > $id_mapped.tmp && mv $id_mapped.tmp $id_mapped                 
```
_#find high similarity seq in the test set using blastpgb_
```
fasta_db='../db/uniprot_sprot.fasta'
formatdb -i $fasta_db
blastpgp -i seeds_filt.fasta -d $fasta_db -m 8 -o blastpgp_results.bl8
```

_#remove them with a py script using a treshold of 95% idenitity_

```
p ../py_scripts/filter_blast_result.py blastpgp_results.bl8 sets/ids_similar95_to_remove 95
sort -u sets/ids_similar95_to_remove > sets/ids_similar95_to_remove.tmp && mv sets/ids_similar95_to_remove.tmp sets/ids_similar95_to_remove
```
_#keep uniq from mapped id and high similarity_
```
sort -u sets/ids_similar95_to_remove $id_mapped > sets/id_to_remove.tmp && mv sets/id_to_remove.tmp sets/id_to_remove
```
_#modify the test set removing training seq_

```
ids_to_remove='sets/id_to_remove'
p ../py_scripts/remove_fasta_by_id.py $ids_to_remove $fasta_db sprot_no_training.fasta
```
### 3.2 Test the model
After that, all the sequences in SP were tested with hmmsearch using the option ‘--max’ which excludes all the heuristic filters. By default, hmmsearch reported in the result only sequences over an E-value threshold of 10. Since the computation of the E-value is influenced by the database search space (Finn et al., 2011), the test was performed once on the entire SP and then the random splitting was applied in order to avoid a bias due to different database size.
```
hmmsearch --cpu 6 --max --noali --tblout hmm_result kunitz.hmm sprot_no_training.fasta
```
_#extract only ID and e-val columns from the hmm result file_
```
grep -v "^#" hmm_result | awk -v OFS="\t" '$1=$1' | cut -f1 | cut -d '|' -f 2 > id_list
grep -v "^#" hmm_result | awk -v OFS="\t" '$1=$1' | cut -f5 > eval_list
paste id_list eval_list > hmm_result && rm id_list eval_list 
```
# 4. E-value optimization and classification benchmark
## 4.1 Generate the two subsets by random spplitting Uniprot
In order to select the E-value maximizing the classification performance, the entire SP ID list was split into 2 subsets, using a python script. The subsets lists were generated randomly of equal length and with the same proportion of Kunitz proteins.

_#download id list of no_kuntiz and kunitz (PF00014) in swissprot_
```
kunitz_ids='sets/kunitz_390.list'
not_kunitz_ids='sets/no_kunitz_569126.list'
tail +2 $not_kunitz_ids  > $not_kunitz_ids.tmp && mv $not_kunitz_ids.tmp $not_kunitz_ids
tail +2 $kunitz_ids  > $kunitz_ids.tmp && mv $kunitz_ids.tmp $kunitz_ids
```

_#remove the training seq from the kunitz id list_
```
grep -vxf $ids_to_remove $kunitz_ids > sets/kunitz_no_training.list
```

_#use the python script to create the subset 1 and 2_
```
p ../py_scripts/random_split.py hmm_result sets/kunitz_no_training.list $not_kunitz_ids sets/subset_1 sets/subset_2 
``` 
#check the uniqness of the ids and that there are no seq in common
```
cut -f1 sets/subset_1 sets/subset_2 | sort -u | wc 
comm -12 <(sort sets/subset_1) <(sort sets/subset_2)
```
## 4.2 E-value optimization and classification benchmark
Subset1 was adopted to select the best threshold and subset2 was adopted as the test set. The role of the 2 subsets was then swapped to cross-validate the results. The 2 subsets lists were annotated with either 1 or 0 depending on the presence of the Kunitz domain according to PFAM and with the E-value previously resulted from hmmsearch. Since the distribution of Kunitz and non-Kunitz was skewed, Matthews’s correlation coefficient (MCC) (2) was adopted as classification score. Compared to accuracy (3) or F1 score, the MCC is a more reliable statistical coefficient which produces a high score only if the prediction obtained good results in all of the four confusion matrix categories (true positives, false negatives, true negatives, and false positives), proportionally both to the size of positive elements and the size of negative elements in the dataset (Chicco and Jurman, 2020; Matthews, 1975).

The classification benchmark was tested by running a python script (Supplementary material) for an E-value threshold decreasing exponentially from 1e-1 to 1e-12. For each subset, the E-value threshold for which the model guaranteed the best MCC was identified, and after that, it was verified that the same outcome was achieved for the other subset. The average between the best threshold for both subset was applied in benchmarking the classification for the entire SP.

_#optimization and classification test on the subsets + lineplot_
```
p ../py_scripts/optimization.py sets/subset_1 sets/subset_2 1e-1 1e-12 > classification_result
```
_#classification on SwissProt_
```
cd sets 
for i in $(seq 1 12);do p ../../py_scripts/classification.py <(cat subset_2 subset_1) 1e-$i;done
```

## References

* Altschul,S.F. et al. (1997) Gapped BLAST and PSI-BLAST: a new generation of protein database search programs. Nucleic Acids Res., 25, 3389–3402.
* Ascenzi,P. et al. The Bovine Basic Pancreatic Trypsin Inhibitor (Kunitz Inhibitor): A Milestone Protein. Curr. Protein Pept. Sci., 4, 231–251.
* Bateman,A. and Haft,D.H. (2002) HMM-based databases in InterPro. Brief. Bioinform., 3, 236–245.
* Berman,H.M. et al. (2000) The Protein Data Bank. Nucleic Acids Res., 28, 235–242. Chen,P. et al. (2013) Collagen VI in cancer and its biological mechanisms. Trend Mol. Med., 19, 410–417.
* Chicco,D. and Jurman,G. (2020) The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation. BMC Genomics, 21, 6.
* Cotabarren,J. et al. (2020) Biotechnological, biomedical, and agronomical applications of plant protease inhibitors with high stability: A systematic review. Plant Sci., 292, 110398.
* Eddy,S.R. (2011) Accelerated Profile HMM Searches. PLOS Comput. Biol., 7,e1002195.
* Finn,R.D. et al. (2011) HMMER web server: interactive sequence similarity searching. Nucleic Acids Res., 39, W29–W37.
* Fries,E. and Kaczmarczyk,A. (2003) Inter-alpha-inhibitor, hyaluronan and inflammation. Acta Biochim. Pol., 50, 735–742.
* Fry,B.G. et al. (2009) The Toxicogenomic Multiverse: Convergent Recruitment of
* Proteins Into Animal Venoms. Annu. Rev. Genomics Hum. Genet., 10, 483–511. Fu,L. et al. (2012) CD-HIT: accelerated for clustering the next-generation sequencing data. Bioinformatics, 28, 3150–3152.
* Hynes,T.R. et al. (1990) X-ray crystal structure of the protease inhibitor domain of
* Alzheimer’s amyloid .beta.-protein precursor. Biochemistry, 29, 10018–10022. Jr,G.J.B. and Girard,T.J. (2012) Tissue factor pathway inhibitor: structure-function. Front. Biosci.-Landmark, 17, 262–280.
* Krissinel,E. and Henrick,K. (2005) Multiple Alignment of Protein Structures in Three Dimensions. In, R. Berthold,M. et al. (eds), Computational Life Sciences, Lecture Notes in Computer Science. Springer, Berlin, Heidelberg, pp. 67–78.
* Lemmer,J.H. et al. (1994) Aprotinin for coronary bypass operations: Efficacy, safety, and influence on early saphenous vein graft patency: A multicenter, randomized, double-blind, placebo-controlled study. J. Thorac. Cardiovasc. Surg., 107, 543– 553.
* Matthews,B.W. (1975) Comparison of the predicted and observed secondary structure of T4 phage lysozyme. Biochim. Biophys. Acta BBA - Protein Struct., 405, 442–451.
* Parkin,S. et al. (1996) Structure of bovine pancreatic trypsin inhibitor at 125 K defi- nition of carboxyl-terminal residues Gly57 and Ala58. Acta Crystallogr. D Biol. Crystallogr., 52, 18–29.
* RAWLINGS,N.D. et al. (2004) Evolutionary families of peptidase inhibitors. Bio- chem. J., 378, 705–716.
* Royston,D. et al. (1987) EFFECT OF APROTININ ON NEED FOR BLOOD TRANSFUSION AFTER REPEAT OPEN-HEART SURGERY. The Lancet, 330, 1289–1291.
* Sabotič,J. and Kos,J. (2012) Microbial and fungal protease inhibitors—current and potential applications. Appl. Microbiol. Biotechnol., 93, 1351–1375.
* Stepek,G. et al. (2010) The kunitz domain protein BLI-5 plays a functionally conserved role in cuticle formation in a diverse range of nematodes. Mol. Biochem. Parasitol., 169, 1–11.
* Wheeler,T.J. et al. (2014) Skylign: a tool for creating informative, interactive logos representing sequence alignments and profile hidden Markov models. BMC Bioinformatics, 15, 7.

