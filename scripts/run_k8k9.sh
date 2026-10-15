#!/usr/bin/env bash
# Usage: nohup ./run_k8k9.sh > run_k8k9.log 2>&1 &
# k = 8 and 9 of the delete design, seed 42, three draws, as in run_seeds.sh on the
# local machine. One chain per draw (k8 then k9); the three chains run in parallel,
# each limited to 40 cpus and 300 GB so the nextflow instances do not oversubscribe.
# Results: <name>_seed42.results. Writes run_k8k9.done when all chains have finished.
set -uo pipefail
cd "$(dirname "$0")"
export NXF_JAVA_HOME=/usr/lib/jvm/java-19-openjdk-amd64   # Nextflow 26.04 needs Java 17+; the login shell may point at 11
unset JAVA_CMD
PIPELINE=$PWD/pipeline   # git checkout of nf-core/taxmarker at acbf705
SEED=42

cat > seed_${SEED}.config <<CFG
process {
    withName: RAXMLNG_SEARCH {
        ext.args = '--fast --seed ${SEED}'
    }
}
executor {
    cpus   = 40
    memory = '300 GB'
}
CFG

run() {
  local name=$1 out=${1}_seed${SEED}.results
  [ -d "$out" ] && { echo "skip $out"; return; }
  nextflow run $PIPELINE -profile docker -c seed_${SEED}.config \
    --sequences ${name}.fna \
    --hmm https://raw.githubusercontent.com/tseemann/barrnap/0.9/db/bac.hmm --hmm_name 16S_rRNA \
    --skip_raxtax true --skip_clustering true \
    --raxmlng_model GTR+FO+I+R10 \
    --outdir "$out" -work-dir work_${name}_seed${SEED} -name ${name}_seed${SEED}_$(date +%s) \
    > ${name}_seed${SEED}.nflog 2>&1
  local rc=$?
  echo "$(date +%T) $name exit $rc"
}

chain() {
  run k8del2$1
  run k9del1$1
}

chain "" &
chain d2 &
chain d3 &
wait
touch run_k8k9.done
