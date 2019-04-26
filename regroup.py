# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 23:14:03 2018

@author: yangq
"""

#This is a script to regroup particles based on the defocus
import sys
import os
if len(sys.argv) < 1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':
    print("Usage: regroup.py input.star")
    exit()
input_file=sys.argv[1]
#Set the basename of the output based on input file
basename=os.path.splitext(input_file)[0]
GroupNumberindex=0
GroupNameindex=0
count=0
with open (input_file,'rw') as input_star:
    with open ("{}_regrouped.star".format(basename),'w') as output_star:
        #Set up the header
        for line in input_star:
            line=line.split(" ")
            if line[0].startswith("_rln") or line[0].startswith("data_") or line[0].startswith("loop_") or line[0]=='\n':
                #Store the variable DefocusV and DefocusV
                if line[0]=="_rlnDefocusV": 
                   newline=line[1].split("#")
                   #global DefocusVindex
                   DefocusVindex=int(newline[1])
                elif line[0]=="_rlnDefocusU":
                    newline=line[1].split("#")
                    #global DefocusUindex
                    DefocusUindex=int(newline[1])
                elif line[0]=="_rlnGroupName":
                    newline=line[1].split("#")
                    #global GroupNameindex
                    GroupNameindex=int(newline[1])
                elif line[0]=="_rlnGroupNumber":
                    newline=line[1].split("#")
                    #global GroupNumberindex
                    GroupNumberindex=int(newline[1])
                head=line
                line=" ".join(line)
                output_star.write(line)
                count+=1
            else:
                break
            #setup GroupNumber and GroupName conditions
        head=head[1].split("#")
        header=int(head[1])
        headerplus=header+1
        headerplusplus=header+2
        #store rest of the file without headers
        temp1=[line.split()for line in input_star]
		#chop off the last '\n'
        temp=temp1[count:-1]
            #Use average Defocus to sort
        temp.sort(key=lambda x:(float(x[DefocusUindex-1])+float(x[DefocusVindex-1]))/2)
        #Default Defocus separation 1000A
        groupnumber=((float(temp[-1][DefocusUindex-1])+float(temp[-1][DefocusVindex-1]))/2-(float(temp[0][DefocusVindex-1])+float(temp[0][DefocusUindex-1]))/2)/1000
        #Find how many particles per group
        Defocus_min=(float(temp[0][DefocusUindex-1])+float(temp[0][DefocusVindex-1]))/2
        if GroupNumberindex!=0 and GroupNameindex==0:
            output_star.write("_rlnGroupName #"+str(headerplus)+"\n")
            group=1
            for line in temp:
                Defocusaverage=(float(line[DefocusUindex-1])+float(line[DefocusVindex-1]))/2
                Defocus_group=Defocus_min+1000*group
                if Defocusaverage<Defocus_group:
                    group=group
                else:
                    group+=1
                line[GroupNumberindex-1]=str(group)  
                line.append('group_{}'.format(group))
                line=" ".join(line)
                output_star.write(' ' + line + '\n')
        elif GroupNumberindex==0 and GroupNameindex!=0:
            output_star.write("_rlnGroupNumber #" +str(headerplus)+"\n")
            group=1
            for line in temp:
                Defocusaverage=(float(line[DefocusUindex-1])+float(line[DefocusVindex-1]))/2
                Defocus_group=Defocus_min+1000*group
                if Defocusaverage<Defocus_group:
                    group=group
                else:
                    group+=1
                line[GroupNameindex-1]='group_{}'.format(group)
                line.append(str(group))
                line=" ".join(line)
                output_star.write(' ' + line + '\n')
        elif GroupNumberindex==0 and GroupNameindex==0:
            output_star.write("_rlnGroupName #" + str(headerplus)+"\n")
            output_star.write("_rlnGroupNumber #" + str(headerplusplus)+"\n")
            group=1
            for line in temp:
                Defocusaverage=(float(line[DefocusUindex-1])+float(line[DefocusVindex-1]))/2
                Defocus_group=Defocus_min+1000*group
                if Defocusaverage<Defocus_group:
                    group=group
                else:
                    group+=1
                line.append('group_{}'.format(group))
                line.append(str(group))
                line=' '.join(line)
                output_star.write(' ' + line + '\n')
        else: 
            group=1
            for line in temp:
                Defocusaverage=(float(line[DefocusUindex-1])+float(line[DefocusVindex-1]))/2
                Defocus_group=Defocus_min+1000*group
                if Defocusaverage<Defocus_group:
                    group=group
                else:
                    group+=1
                line[GroupNameindex-1]='group_{}'.format(group)
                line[GroupNumberindex-1]=str(group)
                line=' '.join(line)
                output_star.write(' ' + line + '\n')
