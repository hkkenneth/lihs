#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012
## Usage: ~/code/bash/20121122_Multi_Seq_Alignment_2_File.sh <ID FILE> <KEYWORD>
set -o verbose


grep ${2} ../result.sorted.appended_len_count.no_0.good_cds.sorted.uniq_cds.new | cut -f 21 | head -n 1 > ${1}
python ~/code/python/003_Fasta_Filter_By_IDs.py ${1} ${1}_seq.fa.1 - /home/klui/x200/03Analysis/FER/31TrinityReDo/Subtract1-6/all_seq/try_map2/good_contig.fa

grep ${2} ../../../../12GoldenStandard/50_fix_gold/20121120_out.txt | cut -f 2 > ${1}

/bin/rm ${1}_clustal_*
while read i
do
	echo $i > ${1}_temp
	python ~/code/python/003_Fasta_Filter_By_IDs.py ${1}_temp ${1}_seq.fa.2 - /home/klui/x200/03Analysis/FER/12GoldenStandard/50_fix_gold/gold1-6.fa

	cat ${1}_seq.fa.1 ${1}_seq.fa.2 > ${1}_seq.fa

	clustalw2 -INFILE=${1}_seq.fa -ALIGN -QUICKTREE -OUTPUT=Clustal -OUTFILE=${1}_clustal_out_temp -STATS=${1}_lustal_stat -ITERATION=TREE -CLUSTERING=UPGMA >> ${1}_clustal_stdout 2>> ${1}_clustal_stderr
	cat ${1}_clustal_out_temp >> ${1}_clustal_out
done < ${1}
