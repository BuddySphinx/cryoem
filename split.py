# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 22:45:49 2018

@author: yangq
"""
#This script is to split particles and save particles for each micrograph
import sys
import os
input_file=sys.argv[1]
count=0
header=[]
temp=[]
with open(input_file,'r') as input_star:
    #store the header to a list
    # Set up the header
    for line in input_star:
            line=line.split(" ")
            if line[0].startswith("_rln") or line[0].startswith("data_") or line[0].startswith("loop_") or line[0]=='\n':
                #Store the variable DefocusV and DefocusV
                if line[0]=="_rlnMicographName": 
                   newline=line[1].split("#")
                   #global DefocusVindex
                   MicrographNameindex=int(newline[1])
                if line[0]=="_rln
                count+=1
                header.append(line)
            else:
                temp.append(line)
                


#with open('test.txt','w') as output_star:
        #for line in temp:
            #line=' '.join(line)
            #output_star.write(line)
        
        #head=head[1].split("#")
        #headernumber=int(head[1])
        #temp=
                
    
