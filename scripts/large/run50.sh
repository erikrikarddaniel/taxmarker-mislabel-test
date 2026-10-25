#!/bin/bash
# usage: run50.sh JOB
j=$1
H=$HOME/projects/taxmarker; O=$H/dnc50
mkdir -p $O/search/$j; cd $O/search/$j
cp $O/parts/$j.fasta $O/parts/$j.nwk .
docker run --rm -u $(id -u):$(id -g) -v $PWD:/w -w /w community.wave.seqera.io/library/raxml-ng:2.0.3--118aed1d80be33ec \
  raxml-ng --search --fast --seed 42 --msa $j.fasta --model GTR+FO+G4m --tree-constraint $j.nwk --threads 2 --prefix $j > search.log 2>&1
[ -f $j.raxml.bestTree ] && DNC_O=$O $H/dnc_run.sh $j $O/search/$j
