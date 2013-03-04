#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 19-12-2012
## Usage: ~/code/r/20121217.sh <SIZE FILE> <CUTOFF>
set -o verbose

R -f ~/code/r/20121219.R --args ${1} ${2}
