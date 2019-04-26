# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:45:19 2019

@author: yangq
"""

#Add argument exercise
import argparse
parser=argparse.ArgumentParser(description="This is an exercise")
parser.add_argument("integer",help="Add an integer",type=int)
parser.add_argument("--verbose","-v",action="count",help="print out information")
args=parser.parse_args()
print(args.integer**2)
if args.verbose>=1:
    print("The process is complicated")

