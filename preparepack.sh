#!/bin/bash

path=.

./prepare-for-viewer.sh $@

filelist=
for NAME in ${path}/batch-run-*
do
    if [ -f ${path}/${NAME}/params.txt ]
    then
	filelist=$(echo $filelist $NAME/plot*.png $NAME/params.txt $NAME/parameters.py $NAME/initial)
    fi
done


rm -f symulacje.zip
zip -r symulacje.zip $filelist viewer.exe

