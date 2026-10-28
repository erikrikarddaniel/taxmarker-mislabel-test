#!/bin/bash
# usage: run_pipeline.sh PIPELINE_REVISION INPUTDIR CLUSTER... ; one run_<cluster>/out per cluster in the current directory.
# INPUTDIR/<cluster>/{sequences.fasta,taxonomy.tsv}; a revision without MAFFT needs INPUTDIR/<cluster>/sequences.fasta already aligned.
rev=$1; in=$2; shift 2
cat > nextflow.config <<'CFG'
process {
    resourceLimits = [ cpus: 4, memory: 12.GB, time: 2.h ]
}
CFG
for t in "$@"; do
  mkdir -p run_$t && cd run_$t
  nextflow run erikrikarddaniel/taxmarker -r "$rev" -profile docker -c ../nextflow.config \
    --sequences $in/$t/sequences.fasta --taxonomy $in/$t/taxonomy.tsv --outdir out > nextflow.stdout 2>&1
  echo "$t exit $?" >> ../finished.txt
  cd ..
done
