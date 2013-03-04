#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 29-11-2012
## Usage: ~/code/r/20121129.sh <LEN FILE>
set -o verbose

R -f ~/code/r/20121129.R --args ${1}
