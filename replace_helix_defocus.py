# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 00:11:33 2018

@author: yangq
"""

#This script is to replace Defocus U,V,A with local refined value for helical particles
import sys
import os
from itertools import groupby
if len(sys.argv)<2 or sys.argv[1]=="--help" or sys.argv[1]=="-h":
    print("Usage: python Replace_defocus.py [particles.star] particle_suffix [replace.star1] [replace.star2]...")
    print(" For example: python Replace_defocus.py _local.star _local.star 2_local.star ....")
particle_file=sys.argv[1]
suffix=sys.argv[2]
local_stars=sys.argv[3:]
header=[]
particles=[]
#setup the header
with open(particle_file,'r') as particle_star:
    for particle in particle_star:
        particle=particle.split(" ")
        if particle[0].startswith("_rln") or particle[0].startswith("data_") or particle[0].startswith("loop_") or particle[0]=='\n':
            if particle[0]=="_rlnMicrographName":
                micrographname=particle[1].split("#")
                MicrographNameindex=int(micrographname[1])-1
            elif particle[0]=="_rlnDefocusU":
                defocusU=particle[1].split("#")
                DefocusUindex=int(defocusU[1])-1
            elif particle[0]=="_rlnDefocusV":
                defocusV=particle[1].split("#")
                DefocusVindex=int(defocusV[1])-1
            elif particle[0]=="_rlnDefocusAngle":
                defocusA=particle[1].split("#")
                DefocusAindex=int(defocusA[1])-1
            elif particle[0]=="_rlnHelicalTubeID":
                helicalID=particle[1].split("#")
                helicalIDindex=int(helicalID[1])-1
            particle=' '.join(particle)
            header.append(particle)
        else:
            newparticle=' '.join(particle)
            newparticle=newparticle.split()
            particles.append(newparticle)
#Write the header to the outputfile
root=os.path.splitext(particle_file)[0]
with open("{}_replaced.star".format(root),'w') as output_star:
    output_star.writelines(header)
#chop off the last \n
if particles[-1]=='\n':
    particles=particles[0:-2]
#Split particle files according to their micrographname
micrograph_particles={name.split("/")[-1].split(".")[0]:list(micrograph_name) for name,micrograph_name in groupby(particles,lambda x:x[MicrographNameindex-1])}
#Replace U,V,A according to the local file
for local_star in local_stars:
    micrograph=local_star.split(suffix)[0]
    try:
        micrograph_particle=micrograph_particles[micrograph]
        helical_particles={ID:list(helix) for ID, helix in groupby(micrograph_particle,lambda x:x[helicalIDindex-1])}
        #Find the keys of the helix dictionary
        IDs=[ID for ID in helical_particles]
        IDs_sorted=sorted(IDs)
        helical_len=[len(helical_particles[ID]) for ID in IDs_sorted]
        local_ps=[]
        with open(local_star,'r') as local_input:
            for local_p in local_input:
                local_p=local_p.split(" ")
                if local_p[0].startswith("_rln") or local_p[0].startswith("data_") or local_p[0].startswith("loop_") or local_p[0]=='\n':
                    if local_p[0]=="_rlnDefocusU":
                        local_defocusU=local_p[1].split("#")
                        local_DefocusUindex=int(local_defocusU[1])-1
                    elif local_p[0]=="_rlnDefocusV":
                        local_defocusV=local_p[1].split("#")
                        local_DefocusVindex=int(local_defocusV[1])-1
                    elif local_p[0]=="_rlnDefocusAngle":
                        local_defocusA=local_p[1].split("#")
                        local_DefocusAindex=int(local_defocusA[1])-1
                else:
                    local_p_new=' '.join(local_p)
                    local_p_new=local_p_new.split()
                    local_ps.append(local_p_new)
        #Record helix ID number
        new_micrograph_particles=[]
        for ID in IDs_sorted:
            local_ID=2*int(ID)-2
            helix_ID=int(ID)-1
            helix_length=int(helical_len[helix_ID])
            #Record the linear difference according to the defocus A,U,Vstart and end of the helix
            diffU=(float(local_ps[local_ID+1][local_DefocusUindex])-float(local_ps[local_ID][local_DefocusUindex]))/helix_length
            diffV=(float(local_ps[local_ID+1][local_DefocusVindex])-float(local_ps[local_ID][local_DefocusVindex]))/helix_length
            diffA=(float(local_ps[local_ID+1][local_DefocusAindex])-float(local_ps[local_ID][local_DefocusAindex]))/helix_length
            for ii in range(0,helix_length):
                #Update the defocus U,V,A for the helical segments
                helical_particles[ID][ii][DefocusUindex]=local_ps[local_ID][local_DefocusUindex]+diffU*ii
                helical_particles[ID][ii][DefocusVindex]=local_ps[local_ID][local_DefocusVindex]+diffV*ii
                helical_particles[ID][ii][DefocusAindex]=local_ps[local_ID][local_DefocusAindex]+diffA*ii
            new_micrograph_particles=new_micrograph_particles.extend(helical_particles[ID])
        #update the micrograph particles
        micrograph_particles[micrograph]=new_micrograph_particles
    except KeyError:
        print("{}.mrc does not exist in your particles".format(micrograph))
        print("make sure your micrographs are consistent in local defocus star file and particle file")
#Output the particles with local defoci values
with open("{}_replaced.star".format(root),'a') as output_star:
    for micrographs,particles in micrograph_particles.items():
        for particle in particles:
            particle=' '.join(particle)
            output_star.write(' ' + particle +'\n')
            
                

    