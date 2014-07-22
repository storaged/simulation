#!/bin/bash

python merge_files.py
R CMD BATCH --vanilla make-heatmap.R
okular plot.png
#exo-open plot.png

