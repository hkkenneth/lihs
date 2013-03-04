#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 25-11-2012
## Usage: ~/code/bash/006_Fastq_PE_Subtraction.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ LIST> <NUM BASES TRIMMED AT 5'> <NUM BASES TRIMMED AT 3'> <INSERT SIZE MIN> <INSERT SIZE MAX>
set -o verbose


index_name=${2}_Temp
bowtie-build --ntoa ${1} $index_name > ${2}_build-stdout 2> ${2}_build-stderr < /dev/null
mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie_opt=""

if [ ${4} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim5 "${4}
fi

if [ ${5} -gt 0 ]
then
	bowtie_opt="$bowtie_opt"" --trim3 "${5}
fi

while read i ; 	read j;
do
	prefix=`basename $i | cut -f 1-4 -d '_'` ;
	bowtie $bowtie_opt --al $prefix"_mapped.fq" --un $prefix"_unmapped.fq" -t -I ${6} -X ${7} --fr -v 1 -p 20 "$index_name" -1 $i -2 $j $prefix"_bowtie_out" > $prefix"_bowtie-stdout" 2> $prefix"_bowtie-stderr" < /dev/null
done < ${3}

/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

