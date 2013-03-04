#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-11-2012
## Usage: ~/code/bash/005_Map_PE_Reads_For_Visualization.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ 1> <FASTQ 2><NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <INSERT SIZE MIN> <INSERT SIZE MAX>
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

touch _BASH_005_START
index_name=${2}_Temp

bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null

mv "$index_name"* /home/klui/install/bowtie-0.12.9/indexes/

bowtie --al ${2}_mapped.fq $bowtie_opt -t -I ${7} -X ${8} --fr -v 1 -p 20 "$index_name" -1 ${3} -2 ${4} ${2}_bowtie_out > ${2}_bowtie-stdout 2> ${2}_bowtie-stderr < /dev/null

bowtie $bowtie_opt -t -k 20 -I ${7} -X ${8} --fr -v 1 -p 20 --sam "$index_name" -1 ${2}"_mapped_1.fq" -2 ${2}"_mapped_2.fq" ${2}_2_bowtie_out.sam > ${2}_2_bowtie-stdout 2> ${2}_2_bowtie-stderr < /dev/null

file_name=${2}_2_bowtie_out.sam
base_name=`basename $file_name .sam`
samtools view -bS $file_name > "$base_name".bam
samtools sort "$base_name".bam "$base_name".sorted
samtools index "$base_name".sorted.bam 

/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_005_END
