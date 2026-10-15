#!/usr/bin/env bash
# Usage: setsid nohup ./run_sets.sh cluster|cluster_raxtax [set ...] > cluster.log 2>&1 &
#   cluster         weighted clustering on, raxtax skipped
#   cluster_raxtax  weighted clustering and raxtax on (the pipeline defaults)
# --fast --seed 42 and GTR+FO+I+R10, as in the sativa-epang-alone runs. Inputs: inputs/<set>.fna.
# Two sets at a time, each Nextflow instance limited to 30 cpus and 150 GB, so one setup uses
# 60 cpus and both setups started together fit in 128. Results: <setup>/<set>_seed42.results.
# Writes <setup>/done when all sets have finished.
set -uo pipefail
cd "$(dirname "$0")"
export NXF_JAVA_HOME=/usr/lib/jvm/java-19-openjdk-amd64   # Nextflow 26.04 needs Java 17+; the login shell may point at 11
unset JAVA_CMD
export NXF_ANSI_LOG=false   # no ANSI console: Nextflow then never calls stty on the terminal, which stops a background run

SETUP=${1:?usage: run_sets.sh cluster|cluster_raxtax [set ...]}
shift
SETS=${*:-k0 k0del10 k3del7 k5del5 k7del3 k8del2 k9del1 k10}
HERE=$PWD
SEED=42
case $SETUP in
  cluster) EXTRA="--skip_raxtax true" ;;
  cluster_raxtax) EXTRA="" ;;
  *) echo "unknown setup $SETUP" >&2; exit 1 ;;
esac

cat > $SETUP/seed_${SEED}.config <<CFG
process {
    withName: RAXMLNG_SEARCH {
        ext.args = '--fast --seed ${SEED}'
    }
}
executor {
    cpus   = 30
    memory = '150 GB'
}
CFG

run() {
  local name=$1 out=${1}_seed${SEED}.results
  cd $HERE/$SETUP
  [ -d "$out" ] && { echo "skip $out"; return; }
  nextflow run $HERE/pipeline -profile docker -c seed_${SEED}.config \
    --sequences $HERE/inputs/${name}.fna \
    --hmm https://raw.githubusercontent.com/tseemann/barrnap/0.9/db/bac.hmm --hmm_name 16S_rRNA \
    $EXTRA \
    --raxmlng_model GTR+FO+I+R10 \
    --outdir "$out" -work-dir work_${name}_seed${SEED} -name ${SETUP}_${name}_$(date +%s) \
    < /dev/null > ${name}_seed${SEED}.nflog 2>&1
  local rc=$?
  echo "$(date +%T) $SETUP $name exit $rc"
}
export -f run
export HERE SETUP SEED EXTRA

printf '%s\n' $SETS | xargs -P 2 -I{} bash -c 'run {}'
touch $SETUP/done
