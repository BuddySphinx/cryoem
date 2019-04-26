#!/bin/tcsh -f
#This is a cshell script to sort particles based on their coordinates. Basically cut out the edge.
#This is a script adopted from Kai
#global setup for output format
set KBold="\x1b\x5b1m"
set KDefault="\x1b\x5b0m"
set KUnderline="\x1b\x5b4m"
set KFlash="\x1b\x5b5m"
#end of global setup 
set args = `printf "$argv" | wc | awk '{print $2}'`
set Proc_name=`echo $0 | awk '{n=split($1,scr,"/");print scr[n];}'`

if ( $args < 2 || $1 == '--help' || $1 == '-h' ) then

        printf "${KBold}Despcription: ${KDefault}This program is used to sort particles based on their X,Y coordinates.\n"
        printf "${KBold}Usage:${KDefault}   $Proc_name particle size in pixels <star file> <pixel size along x axis of the image>,<pixel size along x axis of the image>\n"
        printf "${KBold}example:${KDefault} $Proc_name 100 particle.star 3814 3710\n"
      printf "${KBold}<<<<<  A Kind Reminding: if you find this script useful, please acknowledge Yangqi and Dr.Zhang from Yale.  >>>>>${KDefault}\n"
	exit(1)
endif

set input=$2
set size=$1
set root=`basename $input .star`
set output=${root}_XY_sorted.star
set rlnCoordX=`gawk 'NR<50 && /_rlnCoordinateX/{print $2}' $input |cut -c 2- `
set rlnCoordY=`gawk 'NR<50 && /_rlnCoordinateY/{print $2}' $input |cut -c 2- `

#Find boundary
set X_max=$3
set Y_max=$4

#set X_max=3814
#set Y_max=3740
set X_bound_min=$size
#set X_bound_min=`echo "$size/2" |bc`
#set X_bound_max=`echo "$X_max - $size/2"|bc`
set X_bound_max=`echo "$X_max - $size"|bc`
set Y_bound_min=$size
#set Y_bound_min=`echo "$size/2" |bc`
set Y_bound_max=`echo "$Y_max - $size"|bc`
#set Y_bound_max=`echo "$Y_max - $size/2"|bc`

set headN=`gawk 'NR <100 {if($2 ~ /#/)N=NR;}END{print N}' $input`
gawk 'NR <= '$headN'' $input >$output
#Sort the particles within the boundary
gawk '/mrc/{if( $'$rlnCoordX' > '$X_bound_min' && $'$rlnCoordX' < '$X_bound_max' && $'$rlnCoordY' >'$Y_bound_min' && $'$rlnCoordY' < '$Y_bound_max' ){print $0}}'<$input>>$output





