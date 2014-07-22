#!/bin/bash
for i in `seq 0 31`
do
    scp batch-run-$i/params*.txt kg291538@students.mimuw.edu.pl:~/public_html/TE-model/goeteborg/shuffle-run/$i
    for j in `seq 1 8`
    do
        scp batch-run-$i/plot-$j.png kg291538@students.mimuw.edu.pl:~/public_html/TE-model/goeteborg/shuffle-run/$i/plot-$j.png
    done
done
