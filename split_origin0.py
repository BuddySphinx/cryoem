# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:48:18 2018

@author: yangq
"""

#This file is to split and recenter the particles 
import sys
from itertools import groupby
if len(sys.argv) < 1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':
    print("Usage: split_origin0.py particles.star")
    exit()
input_file=sys.argv[1]
headers=[]
particles=[]
with open(input_file,'r') as input_star:
    # Set up the header
    for particle in input_star:
            particle=particle.split(" ")
            if particle[0].startswith("_rln") or particle[0].startswith("data_") or particle[0].startswith("loop_") or particle[0]=='\n':
                if particle[0]=="_rlnMicrographName": 
                   MicrographName=particle[1].split("#")
                   MicrographNameindex=int(MicrographName[1])-1
                if particle[0]=="_rlnCoordinateX":
                    CoordX=particle[1].split("#")
                    CoordXindex=int(CoordX[1])-1
                if particle[0]=="_rlnCoordinateY":
                    CoordY=particle[1].split("#")
                    CoordYindex=int(CoordY[1])-1
                if particle[0]=="_rlnOriginX":
                    OriginX=particle[1].split("#")
                    OriginXindex=int(OriginX[1])-1
                if particle[0]=="_rlnOriginY":
                    OriginY=particle[1].split("#")
                    OriginYindex=int(OriginY[1])-1
                header=' '.join(particle)
                headers.append(header)
            else:
                particle=' '.join(particle)
                particle_new=particle.split()
                particles.append(particle_new)
if particles[-1]=="\n":
    particles=particles[0:-2]
#Split particles by micrographname
particles_split={micrograph.split("/")[-1].split(".")[0]:list(particle) for micrograph, particle in groupby(particles,lambda x:x[MicrographNameindex])}
micrographs=particles_split.keys()
for micrograph in micrographs:
    with open("{}_split.star".format(micrograph),'w') as split_star:
        split_star.writelines(headers)
        micrograph_particles=particles_split[micrograph]
        #Recenter the coordinates
        for micrograph_particle in micrograph_particles:
            #print(micrograph_particle)
            micrograph_particle[CoordXindex]=str(int(float(micrograph_particle[CoordXindex])))
            micrograph_particle[CoordYindex]=str(int(float(micrograph_particle[CoordYindex])))
            micrograph_particle[OriginXindex]=str(int(float(micrograph_particle[OriginXindex])))
            micrograph_particle[OriginYindex]=str(int(float(micrograph_particle[OriginYindex])))
            micrograph_particle=' '.join(micrograph_particle)
            split_star.write(' '+ micrograph_particle + '\n')

            
        
    

