#!/bin/bash
# usage: subset.sh sh_general_release_dynamic_all_04.04.2024.fasta.gz > viridiplantae.fasta
zcat "$1" | awk 'BEGIN{RS=">";ORS=""} NR>1{split($0,l,"\n"); if (l[1] ~ /\|k__Viridiplantae;/) print ">"$0}'
