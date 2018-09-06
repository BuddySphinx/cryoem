#!/bin/tcsh -f
###
#This program is to regroup particles based on defocus
if ($# != 3) then
 printf "You need input files, split files, input star file, output star file"
 exit 0
if ($# == 3) then
 set split_file = $1
 set input_star = $2
 set root=`basename $input_star .star`
 set output_star=${root}_grouped.star
#Create the header
set header=`gawk '{if($2 ~ /#/)N=NR;}END{print N}' < $input_star`
#This will not print the space
#gawk 'NR<=$header {print $0}' <$input_star>$output_star
gawk 'NR<= '$head'' $input_star>$output_star



