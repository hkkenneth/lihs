# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys
if len(sys.argv) < 1:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

list1 = []
import resource
i = 0
import time
time1 = time.clock()
while i < 1000000000000000000000000000:
	list1.append("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	if i % 1000000000000000:
		time2 = time.clock()
		print time2 - time1
		time1 = time2
		print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
		print resource.getrusage(resource.RUSAGE_SELF).ru_idrss
	i += 1
