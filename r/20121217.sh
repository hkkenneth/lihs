#! /bin/bash
# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 17-12-2012
## Usage: ~/code/r/20121217.sh <E VALUE FILE>
set -o verbose

R -f ~/code/r/20121217.R --args ${1}
