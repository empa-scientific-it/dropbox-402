#!/bin/bash
#Generate a random date
zipname=$(date -d "2000-01-01 + $((RANDOM % 365*20)) days" +%Y%m%d)
tmpfile=$(mktemp /tmp/XXX.txt )
head -1 /dev/random > $tmpfile # just filling the file with garbage, here
tmpfile2=/tmp/$zipname.zip
zip $tmpfile2 $tmpfile 1> /dev/null
echo $tmpfile2
