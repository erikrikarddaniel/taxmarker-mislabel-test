cd ~/projects/taxmarker/blast
mkdir -p results
for q in queries/*.fna; do
  b=$(basename $q .fna)
  docker run --rm -u $(id -u):$(id -g) -v $PWD:/db -w /db -e BLASTDB=/db quay.io/biocontainers/blast:2.17.0--hb02a186_1 \
    blastn -task megablast -db 16S_ribosomal_RNA -query $q -num_threads 8 -max_target_seqs 10 \
    -outfmt '6 qseqid sseqid pident length qcovs bitscore staxids sscinames' -out results/$b.tsv 2> results/$b.err
  echo "done $b $(wc -l < results/$b.tsv)" >> results/progress.log
done
echo finished >> results/progress.log
