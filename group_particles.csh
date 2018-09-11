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
set rlnGroupID=`gawk 'NR <50 &&/_rlnGroupNumber/{print $2}' $input_star | cut -c 2-`
set keyNumber=`gawk 'NR=='$header'{print $2}' $input_star | cut -c 2-`
@ keyGroupName= $keyNumber + 1 
@ Defocus_average_ID= $keyNumber + 1
@ keyGoupID= $keyNumber + 2
#Create a temporary file with
echo "$keyNumber"
echo "$Defocus_average_ID" 
gawk '/mrcs/{for(i=1;i<='$keyNumber';i++)printf("%s ",$i);printf("%f \n", ($'$rlnDefocusUID' + $'$rlnDefocusVID') /2 );}' $input_star |sort -n -k $Defocus_average_ID  > temp.star
#Split the dat file according to defocus, 1000A increment
set Defocus_min=`gawk 'NR==1{printf("%f",$'$Defocus_average_ID');}'< temp.star`
set Defocus_max=`gawk 'END{printf("%f",$'$Defocus_average_ID');}'< temp.star`
set group_num=`echo "(${Defocus_max}-${Defocus_min})/1000" |bc -l |cut -f 1 -d"." `
set particle_num=`gawk 'END{print NR}' temp.star`
set particles_in_group=`echo "($particle_num)/($group_num)" | bc -l`
set NrG=0

if ( $rlnGroupID == "" && !( $rlnGroupNameID == "" ) ) then
 echo "rlnGroupNumber #$keyGroupID" >> $output_star
 while ( $NrG < $group_num )
  #echo "this is good"
  gawk 'NR > ($NrG*$particles_in_group) && NR <=(($NrG+1)*$particles_in_group){for(i=1;i<='$keyNumber';i++){if ( i=='$rlnGroupNameID' ) printf("group_%d ",$NrG+1);else printf("%s ",$i);}printf("%d ",$NrG+1);prinf("\n")}'temp.star >> $output_star
  set NrG = `expr $NrG + 1`
 end
 gawk 'NR >($NrG*$particles_in_group) {for(i=1;i<='$keyNumber';i++){if( i=='$rlnGroupNameID' ) printf("group_%d",$NrG+1);else printf("%s ",$i);}printf("%d ",$NrG+1);printf("\n")}' temp.star >>$output_star

else if ( $rlnGroupNameID == "" && $rlnGroupID == "" ) then
 echo "rlnGroupNameID #$keyGroupName">>$output_star
 echo "rlnGroupNumber #$keyGroupID" >>$output_star
 while ( $NrG < $group_num )
 # echo "this is good"
 gawk 'NR > ($NrG*$particles_in_group) && NR <=(($NrG+1)*particles_in_group){for(i=1;i<='$keyNumber';i++){printf("%s ",$i);}printf("%d ",$NrG+1);printf("group_%d ",$NrG+1);printf("\n")}' temp.star >>$output_star
  set NrG = `expr $NrG + 1` 
 end
 gawk 'NR > ($NrG*particles_in_group) {for(i=1;i<='$keyNumber';i++){printf("%s ",$i);}printf("%d ",$NrG+1);printf("group_%d ",$NrG+1);printf("\n")}' temp.star >>$output_star

else if ( $rlnGroupNameID == "" && !( $rlnGroupID == "" ) ) then
 while ( $NrG < $group_num )
 # echo "this is good"
  gawk 'NR > ($NrG*$particles_in_group) && NR <=(($NrG+1)*particles_in_group){for(i=1;i<='$keyNumber';i++){if (i=='$rlnGroupID') printf("%d ",$NrG+1);else printf("%s ",$i);}printf("group_%d ",$NrG+1);printf("\n")}' temp.star >>output_star
  set NrG = `expr $NrG + 1`
 end
 gawk 'NR > ($NrG*particles_in_group) {for (i=1;i<='$keyNumber';i++){if ( i=='$rlnGroupID' ) printf("%04d ",$NrG+1);else printf("%s ",$i);}printf("group_d% ",$NrG+1);printf("\n")}' temp.star >>$output_star 

else 
 while ( $NrG < $group_num )
  gawk 'NR > ($NrG*particles_in_group)&&NR <=(($NrG+1)*particles_in_group) {for(i=1;i<='$keyNumber';i++){if ( i=='$rlnGroupNameID' ) printf("group_%d ",$NrG+1);else if ( i=='$rlnGroupID' ) printf("%d ",$NrG+1);else printf("%s ",$i);}printf("\n")}' temp.star >>output_star
 # echo "this is good"
  set NrG = `expr $NrG + 1 `
 end
 gawk 'NR > ($NrG*particles_in_group){for(i=1;i<='$keyNumber';i++){if ( i=='$rlnGroupName' ) printf("group_%d ",$NrG+1);else if ( i=='$rlnGroupID' ) printf("%d ",$NrG+1);else printf("%s ",$NrG+1);}printf("\n")}' temp.star>>$output_star
endif

#rm temp.star

