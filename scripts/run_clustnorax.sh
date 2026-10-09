#!/bin/bash
# Usage: ./run_clustnorax.sh NAME -- default clustering, raxtax skipped, --fast seed 42; runs in clustnorax/
cd "$(dirname "$0")/clustnorax" || exit 1
k=$1
nextflow run ~/dev/nf-core-taxmarker -profile docker -c ../seed_42.config \
  --sequences ../${k}.fna \
  --hmm https://raw.githubusercontent.com/tseemann/barrnap/0.9/db/bac.hmm --hmm_name 16S_rRNA \
  --skip_raxtax true \
  --raxmlng_model GTR+FO+I+R10 \
  --outdir ${k}_clustnorax.results -work-dir work_${k}_clustnorax > ${k}_clustnorax.log 2>&1
touch ${k}_clustnorax.done
