#!/bin/bash
# usage: align.sh INPUTDIR CLUSTER... ; aligns INPUTDIR/<cluster>/sequences.fasta to <cluster>.aln.fasta in the current directory
in=$1; shift
for t in "$@"; do
  mafft --auto --preservecase --thread 4 $in/$t/sequences.fasta > $t.aln.fasta
done
