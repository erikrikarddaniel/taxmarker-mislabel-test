#!/bin/bash
O=$HOME/projects/taxmarker/bb; j=bb
cp $O/jobs/bb.nwk $O/jobs/bb.raxml.bestTree
mkdir -p $O/res; cd $O/res
IMG=quay.io/biocontainers/sativa-epang:0.10.2--py314hab16a5f_0
run(){ docker run --rm -u $(id -u):$(id -g) -v $O/jobs:/jobs:ro -v $PWD:/w -w /w $IMG "$@"; }
t0=$(date +%s); lap(){ echo "$1 $(( $(date +%s)-t0 ))s" >> $O/bb.log; }
run sativa-epang -stage reference -s /jobs/$j.fasta -t /jobs/$j.tax -x bac -reftree /jobs/$j.raxml.bestTree -refmodel /jobs/$j.raxml.bestModel -n $j -o . -T 8 > ref.log 2>&1; lap reference
[ -f $j.refjson ] && run sativa-epang -stage loo-tasks -r $j.refjson -n $j -o . > tasks.log 2>&1; lap tasks
[ -d $j.l1o_tasks ] && run sativa-epang -stage loo-place -taskdir $j.l1o_tasks -T 4 > place.log 2>&1; lap place
[ -d $j.l1o_tasks ] && run sativa-epang -stage loo-score -r $j.refjson -n $j -o . -taskdir $j.l1o_tasks > score.log 2>&1; lap score
echo "mis=$(ls $j.mis 2>/dev/null | wc -l)" >> $O/bb.log
echo ALLDONE >> $O/bb.log
