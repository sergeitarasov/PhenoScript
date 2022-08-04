#!/usr/bin/env Rscript --vanilla

args <- commandArgs(trailingOnly = TRUE)
#print(args)

file <- args[1]
file.out <- args[2]
#args <-args[-1]
# all
#stopifnot(action %in% c("-h", "-1", "-2", "-3", "-4"))

if (file=="-h"){
  cat(
    "This script takes Phenoscript dictinary table obtained with cmdPhsDic.R and makes Snippets for Atom.
    Install the Atom packages: r-syntax and snippet-injector.\n
Usage: cmdSnips.R in_phsDic.csv snippets.cson\n
"
  )
  quit()
}
#Options:\n-1 entire file as one block\n-2 each codon separately\n-3 codon 1+2, 3\n-4 codon 1+2, NO 3\n

suppressPackageStartupMessages(library("dplyr"))

#---- Get local dir
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)
source(file.path(script.basename, "snips_functions.R"))
#other.name <- file.path(script.basename, "parser_functions.R")
#source(other.name)
#print(script.basename)
#---- Get local dir

tb <- read.csv(file, stringsAsFactors = FALSE) %>% as_tibble()

### . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ..
### Make snippets                                                           ####
cat('Making Atom snippets....\n')
d1 <-filter(tb, type=='prop')
d2 <-filter(tb, type=='class')
d3 <-filter(tb, type=='data_prop')
s1 <-s2 <- s3 <-  NULL
if (nrow(d1)>0) s1 <- make_snippets(d1, col='#64B5F6', letter='P')
if (nrow(d2)>0) s2 <- make_snippets(d2, col='#FDD835', letter='C')
if (nrow(d3)>0) s3 <- make_snippets(d3, col='#4CAF50', letter='D')

#--- SAVE SNIPPETS TO FILE
# Copy paste the snippets to Atom's snippet.cson
# snippet.cson is located as Atom-> snippets
# add '.source.r': or so
# install Atom package snippet-injector https://atom.io/packages/snippet-injector

#setwd("~/Documents/My_papers/Semantic_discriptions/Protege/Snippets")
snips <- paste0(c(s1,s2,s3), collapse = '')

cat('Writing snippets to: ', file.out, '\n')
# add source etension
snips <- paste0("'.source.r':\n\n", snips)
cat(snips, file=file.out)

#make_one_snippet(d1[1,], col='blue', letter='P')
