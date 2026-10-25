cd ~/projects/taxmarker/blast
docker run --rm -u $(id -u):$(id -g) -v $PWD:/db -w /db -e BLASTDB=/db quay.io/biocontainers/blast:2.17.0--hb02a186_1 \
  blastn -task megablast -db 16S_ribosomal_RNA -query sr/q.fna -num_threads 8 -max_target_seqs 10 \
  -outfmt '6 qseqid sseqid pident length qcovs bitscore staxids sscinames' -out sr/res.tsv 2> sr/res.err
echo finished > sr/done
