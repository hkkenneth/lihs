#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 17-01-2013
## Usage: ~/code/bash/009_Map_PE_SE_Reads_To_Fasta.sh <INPUT FASTA | -> <OUTPUT PREFIX> <FASTQ 1> <FASTQ 2> <NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <INSERT SIZE MIN> <INSERT SIZE MAX> <MAPPED READS | - > <UNMAPPED READS | - >
set -o verbose

bowtie_opt=""

if [ ${5} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim5 "${5}
fi

if [ ${6} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${6}
fi

touch _BASH_009_START
index_name=${2}_Temp

if [ ${1} != "-" ]
then
	bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null
fi

#mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie_opt2=""
bowtie_opt3=""
bowtie_opt4=""
if [  $# -ge 9 ]
then
	if [ ${9} != "-" ]
	then
		bowtie_opt2="--al pe_"${9}".fq"
		bowtie_opt3="--al se_"${9}"_1.fq"
		bowtie_opt4="--al se_"${9}"_2.fq"
	fi
fi

if [  $# -ge 10 ]
then
	if [ ${10} != "-" ]
	then
		bowtie_opt2="$bowtie_opt2"" --un pe_"${10}".fq"
		bowtie_opt3="$bowtie_opt3"" --un se_"${10}"_1.fq"
		bowtie_opt4="$bowtie_opt4"" --un se_"${10}"_2.fq"
	fi
fi

bowtie $bowtie_opt $bowtie_opt2 -t -k 20 -I ${7} -X ${8} --fr -v 1 -p 20 "$index_name" -1 ${3} -2 ${4} ${2}_pe_bowtie_out > ${2}_pe_bowtie-stdout 2> ${2}_pe_bowtie-stderr < /dev/null

bowtie $bowtie_opt $bowtie_opt3 -t -v 1 -p 20 "$index_name" ${3} ${2}_se1_bowtie_out > ${2}_se1_bowtie-stdout 2> ${2}_se1_bowtie-stderr < /dev/null

bowtie $bowtie_opt $bowtie_opt4 -t -v 1 -p 20 "$index_name" ${4} ${2}_se2_bowtie_out > ${2}_se2_bowtie-stdout 2> ${2}_se2_bowtie-stderr < /dev/null

#/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_009_END

#python ~/code/python/008_Bowtie_Count_Hits.py ${2}_bowtie_out ${2}_bowtie_out.count

