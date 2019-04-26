# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 22:45:49 2018

@author: yangq
"""
#This script is to split particles for each micrograph
import sys
if len(sys.argv) < 1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':
    print("Usage: split.py particles.star")
    exit()
input_file=sys.argv[1]
header=[]
temp=[]
with open(input_file,'r') as input_star:
    #store the header to a list
    # Set up the header
    for line in input_star:
            line=line.split(" ")
            if line[0].startswith("_rln") or line[0].startswith("data_") or line[0].startswith("loop_") or line[0]=='\n':
                #Store the variable DefocusV and DefocusV
                if line[0]=="_rlnMicrographName": 
                   newline=line[1].split("#")
                   #global DefocusVindex
                   MicrographNameindex=int(newline[1])
                line=' '.join(line)
                header.append(line)
            
            else:
                line=' '.join(line)
                newline=line.split()
                temp.append(newline)
    #temp=temp[0:-2] #chop off the last space
    #Sort list according to the micrograph
    temp.sort(key=lambda x:x[MicrographNameindex-1])
    MicrographName=""
for i in range(0,len(temp)):
    basename=temp[i][MicrographNameindex-1].split("/")[-1].split(".")[0]
    with open("{}_split.txt".format(basename),'a') as output_star:
        #split the file according to their MicrographName
        if temp[i][MicrographNameindex-1]!=MicrographName:
            output_star.writelines(header)
            line=' '.join(temp[i])
            output_star.write(' ' + line + '\n')
        else:
            line=' '.join(temp[i])
            output_star.write(' ' + line + '\n')
    MicrographName=temp[i][MicrographNameindex-1]