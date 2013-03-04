#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 02-11-2012
## Usage: ~/code/bash/002_Map_PE_Reads_To_Fasta.sh <INPUT FASTA> <OUTPUT PREFIX> <FASTQ 1> <FASTQ 2> <INSERT SIZE MIN> <INSERT SIZE MAX> <MAPPED READS | - > <UNMAPPED READS | - >
set -o verbose

bowtie_opt=""

if [  $# -ge 7 -a "$7" != "-" ]
then
	bowtie_opt="--al ""$7"
fi
if [  $# -ge 8 -a "$8" != "-" ]
then
	bowtie_opt="$bowtie_opt"" --un ""$8"
fi

touch _BASH_002_START
index_name="$2"_Temp

bowtie-build $1 $index_name > "$2"_build-stdout 2> "$2"_build-stderr < /dev/null

mv "$index_name"* /home/klui/install/bowtie-0.12.8/indexes/

bowtie $bowtie_opt --trim5 5 -t -I $5 -X $6 --fr -v 1 -p 20 "$index_name" -1 $3 -2 $4 "$2"_bowtie_out > "$2"_bowtie-stdout 2> "$2"_bowtie-stderr < /dev/null

/bin/rm /home/klui/install/bowtie-0.12.8/indexes/"$index_name"*

touch _BASH_002_END
