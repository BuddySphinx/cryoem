#!/bin/bash
#This is the script to remove bad micrographs
# cd /folder
file=$1
# specify the micrographs number in total
i=$2
j=${#i}
#provides rootname for the micrographs
rootname=$3
if [ $# -lt 1 ]
then 
	echo "You need to input a file"
	exit 0
fi
if [ ! -f $file ]
then 
	echo "You need to provide with a file"
fi 
while IFS= read -r line;do
	printf -v line "%0${j}d" $line
#	echo $line 
	rm "${rootname}${line}.mrc"
done <$file

