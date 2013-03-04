#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012 
## Usage: ~/code/bash/20121122_Loop_Grep_Count.sh <GOLD STANDARD TABLE> <GREP KEYWORD LIST>
# e.g. ~/code/bash/20121122_Loop_Grep_Count.sh ../../../12GoldenStandard/50_fix_gold/20121120_out.txt grep_temp

while read i; do count=`grep -c "$i" ${1}`; echo $i" "$count ; done < ${2}
