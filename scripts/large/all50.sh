cd ~/projects/taxmarker
rm -rf dnc50/search dnc50/res dnc50/dnc.log dnc50/sample.tsv
python3 -I prep50.py
cut -f1 -d' ' dnc50/sample.tsv | xargs -n1 -P4 ./run50.sh
echo ALLDONE >> dnc50/dnc.log
