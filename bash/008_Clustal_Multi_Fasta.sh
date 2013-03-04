#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 08-01-2013
## Usage: ~/code/bash/004_Multi_Seq_Alignment.sh <FASTA FILES ...>
#set -o verbose

val=$RANDOM
echo $val
echo "$@" > "$val".log

cat "$@" > "$val"_seq.fa

clustalw2 -INFILE="$val"_seq.fa -ALIGN -QUICKTREE -OUTPUT=Clustal -OUTFILE="$val"_clustal_out -STATS="$val"_clustal_stat -ITERATION=TREE -CLUSTERING=UPGMA > "$val"_clustal_stdout 2> "$val"_clustal_stderr

