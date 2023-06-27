#!/bin/bash
#Generate a random date
zipname=$(date -d "2000-01-01 + $((RANDOM % 365*20)) days" +%Y%m%d)
tmpdir=/tmp/$zipname
mkdir $tmpdir

# just filling the file with garbage, here
head -1 /dev/random > $tmpdir/data.txt
cp $1 $tmpdir/
echo $tmpdir
