# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 10:47:16 2018

@author: yangq
"""
#This scripte is to intersect defocus of the helical particle along helical tube with linear spacing
#No need to re-extract
#Set up header
import sys
import os
if (sys.argv) <1 or sys.argv[1]=="--help" or sys.argv[1]=="-h":
    print("Usage: python helix_locatctf.py particles.star")
    exit()
input_star=sys.argv[1]
output_basename=os.path.splitext(input_star)[0]
count=0
with open(input_file,'r') as input_star:
    with open ('{}_helixlocalctf.star'.format(output_basename),'w') as output_star:
        #Set up the header
        for line in input_star:
            line=line.split(" ")
            if line[0].startswith("_rln") or line[0].startswith("data_") or line[0].startswith("loop_") or line[0]=='\n':
                #Store Defocus V and Defocus U and MicrographName and helical ID
                if line[0]=="_rlnDefocusU":
                    lineDefocusU=line[1].split("#")
                    Defocusindex=int(lineDefocusU[1])
                elif line[0]=="_rlnDefocusV":
                    lineDefocusV=line[1].split("#")
                    DefocusVindex=int(lineDefocusV[1])
                elif line[0]=="_rlnMicrographName":
                    lineMicrographName=line[1].split("#")
                    MicrographNameindex=int(lineMicrographName[1])
                elif line[0]=="_rlnHelicalTubeID":
                    linehelicaltubeID=line[1].split("#")
                    HelicalTubeIDindex=int(linehelicaltubeID[1])
                    
                    
                    
                
    
