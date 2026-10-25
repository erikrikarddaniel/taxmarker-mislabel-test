cd ~/projects/taxmarker
rm -rf dnc/res dnc/dnc.log
cut -f1,2 dnc/sample.tsv | xargs -n2 -P4 ./dnc_run.sh
echo ALLDONE >> dnc/dnc.log
