#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 16-01-2012
## Usage: ~/code/bash/003_Map_SE_Reads_To_Fasta.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ> <NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <MAPPED READS | - > <UNMAPPED READS | - >
set -o verbose

bowtie_opt=""

if [  $# -ge 6 ]
then
	if [ ${6} != "-" ]
	then
		bowtie_opt="--al "${6}
	fi
fi

if [  $# -ge 7 ]
then
	if [ ${7} != "-" ]
	then
		bowtie_opt="$bowtie_opt"" --un "${7}
	fi
fi

if [ ${4} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim5 "${5}
fi

if [ ${5} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${6}
fi

touch _BASH_003_START
index_name=${2}_Temp

if [ ${1} != "-" ]
then
      bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null
fi

touch _BASH_003_BUILD_DONE

#mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie $bowtie_opt -t -v 1 -p 20 "$index_name" ${3} ${2}_bowtie_out > ${2}_bowtie-stdout 2> ${2}_bowtie-stderr < /dev/null

#/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_003_END

python ~/code/python/008_Bowtie_Count_Hits.py ${2}_bowtie_out ${2}_bowtie_out.count
