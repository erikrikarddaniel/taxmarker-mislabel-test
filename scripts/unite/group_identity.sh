#!/bin/bash
# usage: group_identity.sh UNITEDIR > unite_group_identity.tsv ; UNITEDIR has viridiplantae.fasta and pipeline/<cluster>/taxonomy.tsv
d=$(realpath "$1")
here=$(dirname "$(realpath "$0")")
python3 -I $here/group_identity.py $d/viridiplantae.fasta leichhardtia \
  MW226574,MW226578,MW226603,MW226608,OP251319,OP251326 p__Coniferophyta 1000 f__Apocynaceae 20 /dev/null
sw=$(awk -F'\t' '$2 ~ /g__Swartzia/ {print $1}' $d/pipeline/bryophyta_fabaceae/taxonomy.tsv | tr '\n' ',' | sed 's/,$//')
python3 -I $here/group_identity.py $d/viridiplantae.fasta swartzia $sw p__Bryophyta 60 f__Fabaceae 60 \
  $d/pipeline/bryophyta_fabaceae/taxonomy.tsv | tail -n +2
