#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: ~/code/bash/001_Assembly_Prefix_And_Clean.sh <INPUT FASTA> <ID PREFIX> <OUTPUT FILE PREFIX>
set -o verbose

dir_name=`dirname $1`

python ~/code/python/002_Fasta_Add_Prefix.py $1 $2 "$dir_name"/"$3".prefixed.fasta

python ~/code/python/004_Fasta_Find_Identical_Seq.py "$dir_name"/"$3".prefixed.fasta "$3"
cut -f 2 "$3".python004.list > "$3".exact_seq_id

python ~/code/python/003_Fasta_Filter_By_IDs.py "$3".exact_seq_id "$3".prefixed.duplicate.fasta "$dir_name"/"$3".prefixed.unique.fasta "$dir_name"/"$3".prefixed.fasta

touch _BLAT_START
blat -noHead "$dir_name"/"$3".prefixed.unique.fasta "$dir_name"/"$3".prefixed.unique.fasta blat_output.psl
touch _BLAT_END

python ~/code/python/005_Blat_Find_Internal.py blat_output.psl blat_internal_list > python005.stdout

python ~/code/python/003_Fasta_Filter_By_IDs.py blat_internal_list "$3".prefixed.unique.internal.fasta "$dir_name"/"$3".prefixed.unique.no_internal.fasta "$dir_name"/"$3".prefixed.unique.fasta
