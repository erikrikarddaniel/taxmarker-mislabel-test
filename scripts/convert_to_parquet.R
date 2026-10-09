#!/usr/bin/env Rscript

# convert_to_parquet.R
#
# Converts a single TSV (optionally gzipped) file to Parquet, for pipeline output that
# doesn't already include Parquet copies. Intended to be called once per file from a
# Makefile pattern rule, e.g.:
#
#   %.parquet: %.tsv.gz
#   	Rscript ../scripts/convert_to_parquet.R $< $@
#
# Usage: convert_to_parquet.R infile.tsv[.gz] outfile.parquet

suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(arrow))

args = commandArgs(trailingOnly = TRUE)
if ( length(args) != 2 ) {
    write("Usage: convert_to_parquet.R infile.tsv[.gz] outfile.parquet", stderr())
    quit(status = 1)
}
infile  = args[1]
outfile = args[2]

write_parquet(read_tsv(infile, show_col_types = FALSE), outfile)

# vim: sw=2
