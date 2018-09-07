#!/bin/tcsh -f
###
#This program is to regroup particles based on defocus
#General setup
if ( $#argv != 1 || $1 == "--help"|| $1 == "-h" ) then
 printf "You need input star file \n"
 printf	"Usage:$0 input starfile \n"
 exit 0
endif

set input_star = $1
set root=`basename $input_star .star`
set output_star=${root}_grouped.star
#Create the header
set header=`gawk '{if($2 ~ /#/)N=NR;}END{print N}' < $input_star`
#This will not print the space
#gawk 'NR<=$header {print $0}' <$input_star>$output_star
gawk 'NR<= '$header'' $input_star>$output_star
# split the input file via defocus and sort it
set rlnDefocusUID=`gawk 'NR<50 && /_rlnDefocusU/{print $2}' $input_star | cut -c 2-`
set rlnDefocusVID=`gawk  'NR<50 && /_rlnDefocusV/{print $2}' $input_star | cut -c 2-`
set rlnMicrographName=`gawk 'NR<50 &&/_rlnMicrographName/{print $2}' $input_star | cut -c 2-`
set rlnGroupNameID=`gawk 'NR<50 &&/_rlnGroupName/{print $2}' $input_star | cut -c 2-`
set rlnGroupNumberID=`gawk 'NR <50 &&/_rlnGroupNumber/{print $2}' $input_star | cut -c 2-`
set keyNumber=`gawk 'NR=='header'{print $2}'$input_star | cut -c 2 `
@keyGroupName=$keyNumber + 1 
@keyGroupnumber=$keyNumber + 2
if $rlnGroupName =""

#Create a split file based on Defocus average
gawk '/mrcs/{printf("%s ",$'$rlnMicrographName');printf("%f \n", ($'$rlnDefocusUID' + $'$rlnDefocusVID')/2);}' $input_star | sort -n -k 2 | uniq -f 1 >split.dat
#Split the dat file according to defocus, 1000A increment
set Defocus_min=`gawk 'NR==1{printf("%f",$2);}'< split.dat` 
set Defocus_max=`gawk 'END{printf("%f",$2);}'< split.dat`
set group_num=`echo "(${Defocus_max}-${Defocus_min})/1000" |bc -l |cut -f 1 -d"." `
printf "$group_num, $Defocus_max, $Defocus_min"

