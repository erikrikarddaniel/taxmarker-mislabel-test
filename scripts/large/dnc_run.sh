#!/bin/bash
# usage: dnc_run.sh JOB DIR
j=$1; d=$2
O=${DNC_O:-$HOME/projects/taxmarker/dnc}
mkdir -p $O/res/$j; cd $O/res/$j
cp -L $d/$j.fasta $d/$j.raxml.bestTree $d/$j.raxml.bestModel $O/jobs/
IMG=quay.io/biocontainers/sativa-epang:0.10.2--py314hab16a5f_0
run(){ docker run --rm -u $(id -u):$(id -g) -v $O/jobs:/jobs:ro -v $PWD:/w -w /w $IMG "$@"; }
s=$(date +%s)
run sativa-epang -stage reference -s /jobs/$j.fasta -t /jobs/$j.tax -x bac -reftree /jobs/$j.raxml.bestTree -refmodel /jobs/$j.raxml.bestModel -n $j -o . -T 2 > ref.log 2>&1
[ -f $j.refjson ] && run sativa-epang -stage loo-tasks -r $j.refjson -n $j -o . > tasks.log 2>&1
[ -d $j.l1o_tasks ] && run sativa-epang -stage loo-place -taskdir $j.l1o_tasks -T 2 > place.log 2>&1
[ -d $j.l1o_tasks ] && run sativa-epang -stage loo-score -r $j.refjson -n $j -o . -taskdir $j.l1o_tasks > score.log 2>&1
echo "$j mis=$(ls $j.mis 2>/dev/null | wc -l) secs=$(( $(date +%s)-s ))" >> $O/dnc.log
