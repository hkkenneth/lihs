#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 21-01-2013
## Usage: ~/code/bash/010_Map_PE_SE_Reads_For_Visualization.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ 1> <FASTQ 2> <NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <INSERT SIZE MIN> <INSERT SIZE MAX>
set -o verbose

bowtie_opt=""


if [ ${5} -gt 0 ]
then
	bowtie_opt=" --trim5 "${5}
fi

if [ ${6} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${6}
fi

touch _BASH_010_START
index_name=${2}_Temp

bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null

#mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie --al ${2}_pe_mapped.fq --un ${2}_pe_unmapped.fq $bowtie_opt -t -I ${7} -X ${8} --fr -v 1 -p 20 "$index_name" -1 ${3} -2 ${4} ${2}_pe_bowtie_out > ${2}_pe_bowtie-stdout 2> ${2}_pe_bowtie-stderr < /dev/null

bowtie $bowtie_opt -t -k 20 -I ${7} -X ${8} --fr -v 1 -p 20 --sam "$index_name" -1 ${2}"_pe_mapped_1.fq" -2 ${2}"_pe_mapped_2.fq" ${2}_pe_bowtie_out.sam > ${2}_pe_2_bowtie-stdout 2> ${2}_pe_2_bowtie-stderr < /dev/null

file_name=${2}_pe_bowtie_out.sam
base_name=`basename $file_name .sam`
samtools view -bS $file_name > "$base_name".bam
samtools sort "$base_name".bam "$base_name".sorted
samtools index "$base_name".sorted.bam 

#/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

bowtie --al ${2}_se_mapped.fq $bowtie_opt -t -v 1 -p 20 "$index_name" ${2}_pe_unmapped_1.fq,${2}_pe_unmapped_2.fq ${2}_se_bowtie_out > ${2}_se_bowtie-stdout 2> ${2}_se_bowtie-stderr < /dev/null

# -a allow it to map to all possible alignment
bowtie $bowtie_opt -t -v 1 -p 20 --sam "$index_name" ${2}"_se_mapped.fq" ${2}_se_bowtie_out.sam > ${2}_se_2_bowtie-stdout 2> ${2}_se_2_bowtie-stderr < /dev/null

file_name=${2}_se_bowtie_out.sam
base_name=`basename $file_name .sam`
samtools view -bS $file_name > "$base_name".bam
samtools sort "$base_name".bam "$base_name".sorted
samtools index "$base_name".sorted.bam 

