#!/bin/sh
# Converts Unix txt files into Windows txt file

indirectory=$1
outdirectory="$indirectory/win"
prefix="win"

mkdir $outdirectory
outdirectory="$outdirectory/"

for f in $indirectory/*.txt
do
  filename=${f##*/}
  outfile=$outdirectory$prefix$filename
  #echo $outfile
  touch $outfile
  unix2dos -n $f $outfile
done
