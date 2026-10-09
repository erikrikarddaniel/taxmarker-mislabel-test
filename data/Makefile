SEEDTEST ?= $(HOME)/tmp/seedtest
SCRIPTS   = $(abspath ../scripts)

METRIC_SETS    = k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2 ecsa5 ecsa10 ecsa15 asaia5 asaia10 marm5 marm10
CONSENSUS_SETS = k0 k5 k5d2 k5d3 k10 k10d2 k10d3 k15d1 k15d2 ecsa5 ecsa10 ecsa15
FULL_SETS      = k5 k10 ecsa5 ecsa10 ecsa15

.DELETE_ON_ERROR:
.PHONY: all

all: metrics.tsv consensus.tsv full.tsv

metrics.tsv: $(SCRIPTS)/auguste_metrics.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && python3 $(SCRIPTS)/auguste_metrics.py 0.9 $(METRIC_SETS) > $(CURDIR)/$@

consensus.tsv: $(SCRIPTS)/score.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/score.py k0 | head -n 1; for s in $(CONSENSUS_SETS); do python3 $(SCRIPTS)/score.py $$s | tail -n +2; done; } > $(CURDIR)/$@

full.tsv: $(SCRIPTS)/trace_full.py $(SEEDTEST)/queue3.done
	cd $(SEEDTEST) && { python3 $(SCRIPTS)/trace_full.py $(firstword $(FULL_SETS)) | head -n 1; for s in $(FULL_SETS); do python3 $(SCRIPTS)/trace_full.py $$s | tail -n +2; done; } > $(CURDIR)/$@
