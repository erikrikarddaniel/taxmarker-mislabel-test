SEEDTEST ?= $(HOME)/tmp/seedtest
SCRIPTS   = $(abspath ../scripts)

DELETE_SETS    = k3del7 k3del7d2 k3del7d3 k5del5 k5del5d2 k5del5d3 k7del3 k7del3d2 k7del3d3 k8del2 k8del2d2 k8del2d3 k9del1 k9del1d2 k9del1d3 k0del10
METRIC_SETS    = k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2 ecsa5 ecsa10 ecsa15 asaia5 asaia10 marm5 marm10
CONSENSUS_SETS = k0 k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2 ecsa5 ecsa10 ecsa15
FULL_SETS      = k5 k10 ecsa5 ecsa10 ecsa15
FLAG_SETS      = k0 $(FULL_SETS)
SCORE_SETS     = k3del7 k3del7d2 k3del7d3 k5del5 k5del5d2 k5del5d3 k7del3 k7del3d2 k7del3d3 k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2 ecsa5 ecsa10 ecsa15
REL_SETS       = $(filter-out k0del10 k0 ecsa% asaia% marm%,$(DELETE_SETS)) k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2
MBSCORE       ?=
SETUP_SETS     = k0 k0del10 k3del7 k5del5 k7del3 k8del2 k9del1 k10

.DELETE_ON_ERROR:
.PHONY: all

all: metrics.tsv consensus.tsv full.tsv full_flags.tsv delete_metrics.tsv delete_consensus.tsv setup_flags.tsv relatives.tsv

metrics.tsv: $(SCRIPTS)/auguste_metrics.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && python3 $(SCRIPTS)/auguste_metrics.py 0.9 $(METRIC_SETS) > $(CURDIR)/$@

consensus.tsv: $(SCRIPTS)/score.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/score.py k0 | head -n 1; for s in $(CONSENSUS_SETS); do python3 $(SCRIPTS)/score.py $$s | tail -n +2; done; } > $(CURDIR)/$@

full.tsv: $(SCRIPTS)/trace_full.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/trace_full.py $(firstword $(FULL_SETS)) | head -n 1; for s in $(FULL_SETS); do python3 $(SCRIPTS)/trace_full.py $$s | tail -n +2; done; } > $(CURDIR)/$@

full_flags.tsv: $(SCRIPTS)/full_flags.py $(SEEDTEST)/queue5.done
	cd $(SEEDTEST) && python3 $(SCRIPTS)/full_flags.py 0.9 $(FLAG_SETS) > $(CURDIR)/$@

delete_metrics.tsv: $(SCRIPTS)/auguste_metrics.py $(SEEDTEST)/queue4.done $(SEEDTEST)/k9del1d3_seed42.results/mislabels/user-alignment.mislabels.tsv
	cd $(SEEDTEST) && python3 $(SCRIPTS)/auguste_metrics.py 0.9 $(DELETE_SETS) | grep -v '^k0 vs k0' > $(CURDIR)/$@

delete_consensus.tsv: $(SCRIPTS)/score.py $(SEEDTEST)/queue4.done $(SEEDTEST)/k9del1d3_seed42.results/mislabels/user-alignment.mislabels.tsv
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/score.py k0 | head -n 1; for s in $(DELETE_SETS); do python3 $(SCRIPTS)/score.py $$s $$(case $$s in k[789]*) echo 42;; esac) | tail -n +2; done; } > $(CURDIR)/$@

setup_flags.tsv: $(SCRIPTS)/setup_flags.py $(SEEDTEST)/cluster_raxtax/k10_seed42.results/mislabels/user-alignment.mislabels.tsv
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/setup_flags.py cluster 0.9 $(SETUP_SETS); python3 $(SCRIPTS)/setup_flags.py cluster_raxtax 0.9 $(SETUP_SETS) | tail -n +2; } > $(CURDIR)/$@

relatives.tsv: $(SCRIPTS)/relatives.py $(SEEDTEST)/k9del1d3_seed42.results/mislabels/user-alignment.mislabels.tsv
	cd $(SEEDTEST) && python3 $(SCRIPTS)/relatives.py 0.9 $(REL_SETS) > $(CURDIR)/$@

# MislabelBench's bin/analysis/score_injection.py, not vendored: make mb_score.tsv MBSCORE=/path/to/score_injection.py
mb_score.tsv: $(SCRIPTS)/mb_score.py
	test -n "$(MBSCORE)"
	cd $(SEEDTEST) && python3 $(SCRIPTS)/mb_score.py $(MBSCORE) $(SCORE_SETS) > $(CURDIR)/$@

# Results copied from southern:projects/taxmarker/mb into $(MBCELLS)/<setup>/ (mislabels, gapfilter, clusterselect, checknameconsistency), truth.json files into $(MBCELLS)/truth/
MBCELLS ?= $(HOME)/tmp/mbcells
mb_cells.tsv: $(SCRIPTS)/mb_cells.py
	cd $(MBCELLS) && python3 $(SCRIPTS)/mb_cells.py 0.9 > $(CURDIR)/$@

# Execution traces copied from southern:projects/taxmarker/mb/<setup>/*_seed42.results/pipeline_info/ to $(MBCELLS)/traces/<setup>__<cell>.trace.txt
mb_runtimes.tsv: $(SCRIPTS)/mb_runtimes.py
	cd $(MBCELLS) && python3 $(SCRIPTS)/mb_runtimes.py > $(CURDIR)/$@
