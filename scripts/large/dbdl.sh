mkdir -p ~/projects/taxmarker/blast && cd ~/projects/taxmarker/blast
rm -f dl.log
for f in 16S_ribosomal_RNA taxdb; do
  curl -sSfO https://ftp.ncbi.nlm.nih.gov/blast/db/$f.tar.gz && curl -sSfO https://ftp.ncbi.nlm.nih.gov/blast/db/$f.tar.gz.md5 && md5sum -c $f.tar.gz.md5 >> dl.log 2>&1 && tar xzf $f.tar.gz
done
docker pull quay.io/biocontainers/blast:2.17.0--hb02a186_1 >> dl.log 2>&1
docker run --rm quay.io/biocontainers/blast:2.17.0--hb02a186_1 blastn -version | head -1 >> dl.log 2>&1
ls >> dl.log
echo finished >> dl.log
