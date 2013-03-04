python ~/code/python/003_Fasta_Filter_By_IDs.py ${1} ${1}_seq.fa - ~/x200/04References/DogMouseHuman.protein.verified.fa

clustalw2 -INFILE=${1}_seq.fa -ALIGN -QUICKTREE -OUTPUT=Clustal -OUTFILE=${1}_clustal_out -STATS=${1}_lustal_stat -ITERATION=TREE -CLUSTERING=UPGMA > ${1}_clustal_stdout 2> ${1}_clustal_stderr
