#!/bin/bash
# repeat fold 0 of the 0.97-fixedmodel LOOPLACE task with 8 threads, same input and image
W=/data/users/dl/projects/sbdi-gtdb/taxmarker/work
T=$(ls -d $W/00/410792*)
N=$HOME/projects/taxmarker/noise
rm -rf $N; mkdir -p $N
ln -s "$(readlink -f $T/input)" $N/input
sed 's/-T 12/-T 8/' $T/.command.sh > $N/run.sh
( time docker run --rm --cpus 8 --memory 200g -u $(id -u):$(id -g) \
  -v $W:$W -v $N:$N -w $N quay.io/biocontainers/sativa-epang:0.10.2--py314hab16a5f_0 \
  bash -C -e -u -o pipefail $N/run.sh ) > $N/log.txt 2>&1
echo done >> $N/log.txt
