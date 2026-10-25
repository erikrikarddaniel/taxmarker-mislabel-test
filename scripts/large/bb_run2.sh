#!/bin/bash
O=$HOME/projects/taxmarker/bb; j=bb
cd $O/res
IMG=quay.io/biocontainers/sativa-epang:0.10.2--py314hab16a5f_0
run(){ docker run --rm -u $(id -u):$(id -g) -v $O/jobs:/jobs:ro -v $PWD:/w -w /w $IMG "$@"; }
t0=$(date +%s); lap(){ echo "$1 $(( $(date +%s)-t0 ))s" >> $O/bb.log; }
rm -rf $j.l1o_tasks
run sativa-epang -stage loo-tasks -r $j.refjson -n $j -o . > tasks.log 2>&1; lap tasks2
run sativa-epang -stage loo-place -taskdir $j.l1o_tasks -T 8 > place.log 2>&1; lap place2
run sativa-epang -stage loo-score -r $j.refjson -n $j -o . -taskdir $j.l1o_tasks > score.log 2>&1; lap score2
echo "mis=$(ls $j.mis 2>/dev/null | wc -l)" >> $O/bb.log
echo ALLDONE >> $O/bb.log
