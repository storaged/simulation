#!/bin/bash
for i in $(seq $1 $2)
do
	sh run-sim-"$i".sh
done
echo "done $1-$2" >&2
date >&2
