#!/bin/bash
# usage: sweep.sh ID [ID...]  -- count (cluster,taxon) pairs per vsearch identity, same command as VSEARCH_CLUSTER
W=/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter
O=$HOME/projects/taxmarker/sweep
mkdir -p $O
for id in "$@"; do
  s=$(date +%s)
  docker run --rm -u $(id -u):$(id -g) -v $W:/in:ro -v $O:/out community.wave.seqera.io/library/samtools_vsearch:8a419aba60edb7b2 \
    vsearch --cluster_fast /in/user-alignment.weightfiltered.ungapped.fasta --uc /out/id$id.uc --threads 8 --id $id --quiet
  e=$(date +%s)
  awk -F'\t' -v id=$id -v t=$((e-s)) 'FNR==NR{n=index($0,"\t"); tax[substr($0,1,n-1)]=substr($0,n+1); next}
    $1=="S"||$1=="H"{k[$2"\t"tax[$9]]=1; c[$2]=1}
    END{p=0; for(x in k)p++; q=0; for(x in c)q++; print id, "clusters="q, "reps="p, "vsearch_s="t}' \
    $W/user-alignment.weightfiltered.tax $O/id$id.uc >> $O/sweep.tsv
  echo "done $id" >> $O/sweep.log
done
