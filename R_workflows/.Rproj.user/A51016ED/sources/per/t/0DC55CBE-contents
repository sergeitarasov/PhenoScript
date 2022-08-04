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
    "This script takes an ontology file using ROBOT and produces a csv table. Rows: classes, OP, DP; Cols: IRI, Defs, Labels.
    This table can be used in Phenoscript and Atom snippets.\n
Usage: cmdPhsDic in_ontology.xml out.csv\n
"
  )
  quit()
}
#Options:\n-1 entire file as one block\n-2 each codon separately\n-3 codon 1+2, 3\n-4 codon 1+2, NO 3\n

#---- Get local dir
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)
#other.name <- file.path(script.basename, "other.R")
#source(other.name)
#print(script.basename)
#---- Get local dir

suppressPackageStartupMessages(library("dplyr"))
suppressPackageStartupMessages(library(stringr))
#source('parser_functions.R')
#file.path(script.basename, "parser_functions.R")

#---- Execute Robot with Sparql
cat('Executing robot for: ', file, '\n')
out_tmp <- tempdir()
#unlink()
#print(out_tmp)
#robot query --input aism_instances.xml \--queries get_class.sparql get_op.sparql get_dp.sparql \--output-dir results/
#system('robot query --input aism_instances.xml \\--queries get_class.sparql get_op.sparql get_dp.sparql \\--output-dir results/')
q1 <- file.path(script.basename, 'get_class.sparql')
q2 <- file.path(script.basename, 'get_op.sparql')
q3 <- file.path(script.basename, 'get_dp.sparql')
q <- paste(q1, q2, q3, sep=' ')
#exec_robot <- paste0('robot query --input ', file, ' \\--queries get_class.sparql get_op.sparql get_dp.sparql \\--output-dir ', out_tmp, '/')
exec_robot <- paste0('robot query --input ', file, ' \\--queries ', q, ' \\--output-dir ', out_tmp, '/')
# cat(paste0(script.basename, '\n'))
# exec_robot <- paste0('robot query --input ', file, ' \\--queries ', q, ' \\--output-dir ', script.basename, '/')

system(exec_robot)


#---- Read in Sparql queries
# cl <- read.csv('results/get_class.csv', stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='class')
# dp <- read.csv('results/get_dp.csv', stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='data_prop')
# op <- read.csv('results/get_op.csv', stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='prop')

cl <- read.csv(file.path(out_tmp, 'get_class.csv'), stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='class')
dp <- read.csv(file.path(out_tmp, 'get_dp.csv'), stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='data_prop')
op <- read.csv(file.path(out_tmp, 'get_op.csv'), stringsAsFactors = FALSE) %>% as_tibble() %>% mutate(type='prop')
#write.csv(dp, file='dp_testtt.csv')

tb <- bind_rows(cl, dp, op)
colnames(tb) <- c('IRI', 'label', 'Defs', 'type')
print(tb)

# !!! What we sjould remove them??
# remove ID with no httpp
tb <- tb[str_detect(tb$IRI, 'http:'),]

#make ID short
#str_split('http://purl.obolibrary.org/obo/AISM_000', '/')
x <- str_split(tb$IRI, '/')
ID.short <- lapply(x, function(y) {y[length(y)]}) %>% unlist
tb <- mutate(tb, ID.short=ID.short, ID=ID.short)

# namespaces
nm <- lapply(x, function(y) { y[1:(length(y)-1)]} %>% paste0(., collapse = '/') ) %>% unlist
cat('Unique namespaces: ', unique(nm), '\n')


### . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ..
### Filter/change terms for output                                          ####

# if lable is na then put ID
tb <-tb %>% mutate(label.final=replace(label, label=='na', filter(tb, label=='na')$ID))
#filter(tb, label=='na')
# filter(tb, label=='')

# make no space labels
tb <-tb %>% mutate(label.nospace=gsub(" ", "_", label.final))

# remove space in lablel.final as well
tb <-tb %>% mutate(label.final=gsub(" ", "_", label.final))

# add dot to properties and data_props
# tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='prop', paste0(filter(tb, type=='prop')$label.nospace, '.') ))
# tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='data_prop', paste0(filter(tb, type=='data_prop')$label.nospace, '.') ))
tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='prop', paste0('.', filter(tb, type=='prop')$label.nospace) ))
tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='data_prop', paste0('.', filter(tb, type=='data_prop')$label.nospace) ))
#paste0(filter(all, type=='prop')$label.nospace, '.')
#filter(all, type=='prop')

# # add attibutes '($1)$2)' to props and data_props
# tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='prop', paste0(filter(tb, type=='prop')$label.nospace, '($1)$2' )))
# tb <-tb %>% mutate(label.nospace=replace(label.nospace, type=='data_prop', paste0(filter(tb, type=='data_prop')$label.nospace, '($1)$2' )))
# #filter(all, type=='prop')

# dupicates
# reomve duplicates in ID
tb <-distinct(tb, ID, .keep_all = TRUE)
cat('Removing duplicated iri... Duplicated iri: ', any(duplicated(tb$ID)), '\n')

# rsolve duplicates in label
cat('Duplicated labels: ', any(duplicated(tb$label.final)), '\n')
dup <- tb$label[duplicated(tb$label)]
dup.id <- which(!is.na(match(tb$label, dup))==TRUE)
#tb[dup.id,]
iri <- c(tb[dup.id,'ID.short'])[[1]]
lf <- c(tb[dup.id,'label.final'])[[1]]
ls <- c(tb[dup.id,'label.nospace'])[[1]]
tb[dup.id,'label.final'] <- paste0(lf,'[iri="', iri, '"]')
tb[dup.id,'label.nospace'] <- paste0(ls,'[iri="', iri, '"]')

cat('Resolving.. Duplicated labels: ', any(duplicated(tb$label.final)), '\n')

# change unwanted symbols i.e, ' to \'
tb <-tb %>% mutate(Defs=gsub("\'", "\\\\'", Defs), label.final=gsub("\'", "\\\\'", label.final),
                   label.nospace=gsub("\'", "\\\\'", label.nospace) )

### . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ..
### Write translatopn to tb                                                  ####

cat('Writing dictionary to: ', file.out, '\n')
write.csv(tb, file=file.out)

