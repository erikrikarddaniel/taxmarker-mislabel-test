#!/bin/bash
# Usage: ./run_full.sh "k5 k10" -- default clustering and raxtax, --fast seed 42
for k in $1; do
  out=${k}_full.results
  [ -d "$out" ] && continue
  nextflow run ~/dev/nf-core-taxmarker -profile docker -c seed_42.config \
    --sequences ${k}.fna \
    --hmm https://raw.githubusercontent.com/tseemann/barrnap/0.9/db/bac.hmm --hmm_name 16S_rRNA \
    --raxmlng_model GTR+FO+I+R10 \
    --outdir "$out" -work-dir work_${k}_full > ${k}_full.log 2>&1
done
