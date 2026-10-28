#!/bin/bash
# usage: subset.sh sh_general_release_dynamic_all_04.04.2024.fasta.gz [k__Viridiplantae] > viridiplantae.fasta
zcat "$1" | awk -v k="${2:-k__Viridiplantae}" 'BEGIN{RS=">";ORS=""} NR>1{split($0,l,"\n"); if (index(l[1], "|" k ";")) print ">"$0}'
