#!/usr/bin/env bash
# Usage: ./run_seeds.sh "k0 k5 asaia10" "42 43 44"   (names of <name>.fna)
# One pipeline run per (k, seed). Fast search, fixed model, raxtax and clustering off,
# so every injected sequence reaches SATIVA. Results in <name>_seed<seed>.results.
set -euo pipefail
cd "$(dirname "$0")"
for k in $1; do
  for seed in $2; do
    out=${k}_seed${seed}.results
    [ -d "$out" ] && { echo "skip $out"; continue; }
    cat > seed_${seed}.config <<EOF
process {
    withName: RAXMLNG_SEARCH {
        ext.args = '--fast --seed ${seed}'
    }
}
EOF
    nextflow run ~/dev/nf-core-taxmarker -profile docker -c seed_${seed}.config \
      --sequences ${k}.fna \
      --hmm https://raw.githubusercontent.com/tseemann/barrnap/0.9/db/bac.hmm --hmm_name 16S_rRNA \
      --skip_raxtax true --skip_clustering true \
      --raxmlng_model GTR+FO+I+R10 \
      --outdir "$out" -work-dir work_${k}_seed${seed}
  done
done
