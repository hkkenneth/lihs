#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 19-11-2012
## Usage: ~/code/bash/002c_Map_PE_Reads_To_Fasta.sh <INPUT FASTA | -> <OUTPUT PREFIX> <FASTQ 1> <FASTQ 2><NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <INSERT SIZE MIN> <INSERT SIZE MAX> <MAPPED READS | - > <UNMAPPED READS | - >
set -o verbose

bowtie_opt=""

if [  $# -ge 9 ]
then
	if [ ${9} != "-" ]
	then
		bowtie_opt="--al "${9}
	fi
fi

if [  $# -ge 10 ]
then
	if [ ${10} != "-" ]
	then
		bowtie_opt="$bowtie_opt"" --un "${10}
	fi
fi

if [ ${5} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim5 "${5}
fi

if [ ${6} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${6}
fi

touch _BASH_002c_START
index_name=${2}_Temp

if [ ${1} != "-" ]
then
	bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null
fi

#mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie $bowtie_opt -t -k 20 -I ${7} -X ${8} --fr -v 1 -p 20 "$index_name" -1 ${3} -2 ${4} ${2}_bowtie_out > ${2}_bowtie-stdout 2> ${2}_bowtie-stderr < /dev/null

#/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_002c_END

python ~/code/python/008_Bowtie_Count_Hits.py ${2}_bowtie_out ${2}_bowtie_out.count
