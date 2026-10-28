#!/bin/bash
# usage: cluster.sh viridiplantae.fasta MMSEQS_BINARY; run in the directory for the output
m=${2:-mmseqs}
$m version > mmseqs.version
for id in 0.99 0.97 0.95 0.90 0.85 0.80 0.75; do
  $m easy-cluster "$1" mmc$id tmp_c --min-seq-id $id -c 0.8 --cov-mode 0 --threads 8 -v 1 > mmc$id.log 2>&1
  rm -rf tmp_c
done
