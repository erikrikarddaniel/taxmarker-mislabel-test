#!/usr/bin/env bash
# Usage: setsid ./run_mb.sh > run_mb.log 2>&1 < /dev/null &
# MislabelBench cells (family distance, rate 0.05, seed 1, k = 1 2 3 5 10) plus the un-injected base
# (gtdb_arc2k.tax), through three taxmarker setups: alone (clustering and raxtax off), cluster
# (clustering on, raxtax off) and cluster_raxtax (pipeline defaults). --fast --seed 42, GTR+FO+I+R10.
# Four runs at a time, 30 cpus and 150 GB each. Results: <setup>/<cell>_seed42.results; writes done when finished.
set -uo pipefail
cd "$(dirname "$0")"
export NXF_JAVA_HOME=/usr/lib/jvm/java-19-openjdk-amd64
unset JAVA_CMD
export NXF_ANSI_LOG=false
export PATH=$HOME/bin:$PATH
HERE=$PWD
BENCH=$HERE/../mislabelbench
SEED=42
CELLS="base inj_family_r0.05_k1_s1 inj_family_r0.05_k2_s1 inj_family_r0.05_k3_s1 inj_family_r0.05_k5_s1 inj_family_r0.05_k10_s1"
SETUPS="alone cluster cluster_raxtax"
mkdir -p $SETUPS
cat > seed_${SEED}.config <<CFG
process {
    withName: RAXMLNG_SEARCH {
        ext.args = "--fast --seed ${SEED}"
    }
}
executor {
    cpus   = 30
    memory = "150 GB"
}
CFG

run() {
  local setup=$1 cell=$2 out=${2}_seed${SEED}.results extra tax
  case $setup in
    alone) extra="--skip_raxtax true --skip_clustering true" ;;
    cluster) extra="--skip_raxtax true" ;;
    cluster_raxtax) extra="" ;;
  esac
  if [ $cell = base ]; then tax=$BENCH/data/gtdb/gtdb_arc2k.tax; else tax=$BENCH/data/injected/$cell/$cell.tax; fi
  mkdir -p $HERE/$setup/run_$cell && cd $HERE/$setup/run_$cell
  [ -d "$HERE/$setup/$out" ] && { echo "skip $setup $cell"; return; }
  nextflow run $HERE/../pipeline -profile docker -c $HERE/seed_${SEED}.config \
    --sequences $BENCH/data/gtdb/gtdb_arc2k.fasta --taxonomy $tax $extra \
    --raxmlng_model GTR+FO+I+R10 \
    --outdir "$HERE/$setup/$out" -work-dir $HERE/$setup/work_${cell}_seed${SEED} -name mb_${setup}_$(echo $cell | tr -c a-z0-9 _)$(date +%s) \
    < /dev/null > $HERE/$setup/${cell}_seed${SEED}.nflog 2>&1
  local rc=$?
  echo "$(date +%T) $setup $cell exit $rc"
}
export -f run
export HERE BENCH SEED

for c in $CELLS; do for s in $SETUPS; do echo "$s $c"; done; done | xargs -P 4 -L 1 bash -c "run \$0 \$1"
touch done
