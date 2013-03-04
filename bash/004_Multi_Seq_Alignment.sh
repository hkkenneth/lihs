#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 12-11-2012
## Usage: ~/code/bash/004_Multi_Seq_Alignment.sh <ID LIST> <FASTA>
set -o verbose

python ~/code/python/003_Fasta_Filter_By_IDs.py ${1} ${1}_seq.fa - ${2}

clustalw2 -INFILE=${1}_seq.fa -ALIGN -QUICKTREE -OUTPUT=Clustal -OUTFILE=${1}_clustal_out -STATS=${1}_clustal_stat -ITERATION=TREE -CLUSTERING=UPGMA > ${1}_clustal_stdout 2> ${1}_clustal_stderr
