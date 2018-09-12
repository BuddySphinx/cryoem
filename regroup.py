# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 23:14:03 2018

@author: yangq
"""

#This is a script to group particles 
import sys
import os
input_file=sys.argv[1]
output_file=sys.argv[2]
GroupNumberindex=0
GroupNameindex=0
#os.system('touch -f $2')
#write the header to the output file
#global DefocusUindex
#DefocusUindex=0
count=0
with open (input_file,'rw') as input_star:
    with open (output_file,'w') as output_star:
        #Set up the header
        for line in input_star:
            line=line.split(" ")
            if line[0].startswith("_rln") or line[0].startswith("data_") or line[0].startswith("loop_") or line[0]=="\n":
                #Store the variable DefocusV and DefocusV
                if line[0]=="_rlnDefocusV": 
                   newline=line[1].split("#")
                   #global DefocusVindex
                   DefocusVindex=int(newline[1])
                elif line[0]=="_rlnDefocusU":
                    newline=line[1].split("#")
                    #global DefocusUindex
                    DefocusUindex=newline[1]
                elif line[0]=="_rlnGroupName":
                    newline=line[1].split("#")
                    #global GroupNameindex
                    GroupNameindex=newline[1]
                elif line[0]=="_rlnGroupNumber":
                    newline=line[1].split("#")
                    #global GroupNumberindex
                    GroupNumberindex=newline[1]
                line=" ".join(line)
                output_star.write(line)
                count+=1
            else:
                break
            #setup GroupNumber and GroupName conditions
        header=count
        headerplus=count+1
        headerplusplus=count+2
        if GroupNumberindex!=0 and GroupNameindex==0:
            output_star.write("_rlnGroupName #"+str(headerplus)+"\n")
            #Fill the code and sort
           
        elif GroupNumberindex==0 and GroupNameindex!=0:
            output_star.write("_rlnGroupNumber #" +str(headerplus)+"\n")
        elif GroupNumberindex==0 and GroupNameindex==0:
            output_star.write("_rlnGroupName #" + str(headerplus)+"\n")
            output_star.write("_rlnGroupNumber #" + str(headerplusplus)+"\n")
        else:
            
            #output
#print(DefocusVindex)
print(GroupNumberindex)
#print(GroupNameindex)
       
        #temp=[line for line in input_star]
                 
                
            
            
            
    