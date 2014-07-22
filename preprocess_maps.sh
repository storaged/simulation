#!/bin/bash

#przygotowanie map dla symulacji. wszystkie mapy musza byc w katalogu maps

cd maps
for img in $(ls | grep -vE '(.tmp|.svg|.xcf)')
do
	echo $img
	#pypy can't import Image
	python ../preprocess_map.py $img
done
