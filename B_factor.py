#!/usr/bin/env python
import os
import sys
import math
global Num
Num=float(sys.argv[1])
Cat=sys.argv[2]
if Cat=="B":
	std=Num/(math.pi**2*8)
	res=math.exp(-(2.0548-math.log(Num))/1.8169)
	print "The standard deviation is {0:.3f}".format(std)
	print "The resolution is {0:.3f}".format(res)
elif Cat=="RES":
	B=math.exp(2.0548+1.8169*math.log(Num))
	std=B/(8*math.pi**2)
	print "The standard deviation is {0:.3f}".format(std)
	print "The B factor is {0:.3f}".format(B)
else:
	B=Num**2*8*math.pi**2
	res=math.exp(-(2.0528-math.log(B))/1.8169)
	print "The B factor is {0:.3f}".format(B)
	print "The resolution is {0:.3f}".format(res)

	
	
