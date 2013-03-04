#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 08-11-2012
## Usage: ~/code/r/001sh_Line_Plot_Abs.sh <MIN> <MAX> <COUNT>
set -o verbose

R -f ~/code/r/001_Line_Plot_Abs.R --args ${1} ${2} ${3}
