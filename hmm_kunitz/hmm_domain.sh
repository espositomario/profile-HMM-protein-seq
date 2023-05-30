#!/bin/sh
# this pipeline is designed to model protein domain hrough HMM
# some steps require to browser manually websites/webtools
# It's designed using python 3.10 
# conda create -n <env_name> blast blast-legacy hmmer cd-hit # -c Bioconda
fasta_db='../db/uniprot_sprot.fasta'
# With PDBeFold search for similar structures to BPT1 and filter with Q-score > 0.75 (#seq = 305)
fasta_similar_structure='bpt1_result_qscore_0.75.fasta.seq'
# exclude identical sequences! I choose 1 (77 clusters) as treshold because using 0.98 (33 clusters) in the end the classification resulted with a 1 more false positive ['P84555'].
# maybe keeping also sequences differing for only one residue make the hmm more precise. (#seq = 77)
cd-hit -i $fasta_similar_structure -o seeds_filt.fasta -c 1
# extract pdb id with chain to align the structures on pdbefold
grep  '^>' seeds_filt.fasta | cut -d' ' -f1 | cut -c6- > sets/pdb_id_training.list
# multi align on pdbefold by pdb id list (#seq = 77)
https://www.ebi.ac.uk/msd-srv/ssm/
# download the msa.fasta file
#-------------------------------------------------------------------------------------------------------------------------------
msa='msa_seeds.seq'
# remove empty line
grep . $msa > $msa.tmp && mv $msa.tmp $msa 
# no trimming, leaving hmmbuild to choose the best trimming
# grep . seeds_msa.fasta | awk '{if (substr($1,1,1)==">") {printf "\n%s ",$1} else {printf "%s",$0}}' | awk '{print $1;print substr($2,9,58)}' > kunitz_pdb_msa_trim.fasta
hmmbuild kunitz.hmm $msa
# visualize on skylign the hmm
# download id list of no_kuntiz and kunitz (PF00014) in swissprot
#-----------------------------------------------------------------------------------------
kunitz_ids='sets/kunitz_390.list'
not_kunitz_ids='sets/no_kunitz_569126.list'
# remove col name
tail +2 $not_kunitz_ids  > $not_kunitz_ids.tmp && mv $not_kunitz_ids.tmp $not_kunitz_ids
tail +2 $kunitz_ids  > $kunitz_ids.tmp && mv $kunitz_ids.tmp $kunitz_ids
# check seq number and ids number
# grep -o '^>' kunitz_390.fasta|wc
# grep -o '^>' no_kunitz_569126.fasta|wc
# wc < $kunitz_id
# wc < $not_kunitz_id
# remove the protein used for training hmm mapping pdb id to uniprot/swissprot (sets/pdb_id_training.list)
# Uniprot ID Mapping
https://www.uniprot.org/id-mapping
# 71 IDs were mapped to 71 results
# 6 ID were not mapped:
# 3ci7:A,6har:E,3l3t:E,3aue:C,5nx3:C,3auc:A
# 16 unique IDs
id_mapped='sets/id_mapped.list'
# remove header
tail +2 $id_mapped | cut -f 2 > $id_mapped.tmp && mv $id_mapped.tmp $id_mapped                 
#-----------------------------------------------------------------------------------------------------------
############find high similarity seq in the test set(SwissProt) using blastpgb  (for a fail test of the HMM) 
formatdb -i $fasta_db
blastpgp -i seeds_filt.fasta -d $fasta_db -m 8 -o blastpgp_results.bl8
# remove them with a py script using a treshold of 95% idenitity
p ../py_scripts/filter_blast_result.py blastpgp_results.bl8 sets/ids_similar95_to_remove 95
sort -u sets/ids_similar95_to_remove > sets/ids_similar95_to_remove.tmp && mv sets/ids_similar95_to_remove.tmp sets/ids_similar95_to_remove
# keep uniq from mapped id and high similarity
sort -u sets/ids_similar95_to_remove $id_mapped > sets/id_to_remove.tmp && mv sets/id_to_remove.tmp sets/id_to_remove
# modify swisspprot db removing training seq (#seq removed = 30) (#seq in SwissProt = 569516-30 = 569486)
ids_to_remove='sets/id_to_remove'
p ../py_scripts/remove_fasta_by_id.py $ids_to_remove $fasta_db sprot_no_training.fasta
# test the model
hmmsearch --cpu 6 --max --noali --tblout hmm_result kunitz.hmm sprot_no_training.fasta
# extract only ID and e-val columns from the hmm result file
grep -v "^#" hmm_result | awk -v OFS="\t" '$1=$1' | cut -f1 | cut -d '|' -f 2 > id_list
grep -v "^#" hmm_result | awk -v OFS="\t" '$1=$1' | cut -f5 > eval_list
paste id_list eval_list > hmm_result && rm id_list eval_list 
# remove the training seq from the kunitz id list (#seq = 390-30 = 360)
grep -vxf $ids_to_remove $kunitz_ids > sets/kunitz_no_training.list
# use the python script to create the subset 1 and 2
p ../py_scripts/random_split.py hmm_result sets/kunitz_no_training.list $not_kunitz_ids sets/subset_1 sets/subset_2 
# check the uniqness of the ids
cut -f1 sets/subset_1 sets/subset_2 | sort -u | wc 
# check that there are no seq in common between the 2 subsets
comm -12 <(sort sets/subset_1) <(sort sets/subset_2)
# do the optimization on the subsets
p ../py_scripts/optimization.py sets/subset_1 sets/subset_2 1e-1 1e-12 
# do the classification on SwissProt
cd sets 
for i in $(seq 1 12);do p ../../py_scripts/classification.py <(cat subset_2 subset_1) 1e-$i;done
