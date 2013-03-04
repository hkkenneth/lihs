#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 28-11-2012
## Usage: ~/code/bash/007_Map_SE_Reads_For_Visualization.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ> <NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'>
set -o verbose

bowtie_opt=""


if [ ${4} -gt 0 ]
then
	bowtie_opt=" --trim5 "${4}
fi

if [ ${5} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${5}
fi

touch _BASH_007_START
index_name=${2}_Temp

bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null

mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie --al ${2}_mapped.fq $bowtie_opt -t -v 1 -p 20 "$index_name" ${3} ${2}_bowtie_out > ${2}_bowtie-stdout 2> ${2}_bowtie-stderr < /dev/null

# -a allow it to map to all possible alignment
bowtie $bowtie_opt -t -a -v 1 -p 20 --sam "$index_name" ${2}"_mapped.fq" ${2}_2_bowtie_out.sam > ${2}_2_bowtie-stdout 2> ${2}_2_bowtie-stderr < /dev/null

file_name=${2}_2_bowtie_out.sam
base_name=`basename $file_name .sam`
samtools view -bS $file_name > "$base_name".bam
samtools sort "$base_name".bam "$base_name".sorted
samtools index "$base_name".sorted.bam 

/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_007_END
