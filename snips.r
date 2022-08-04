#!/usr/bin/env Rscript --vanilla

args <- commandArgs(trailingOnly = TRUE)
#print(args)

file <- args[1]
file.out <- args[2]
update.arg <- args[3]


if (file=="-h"){
  cat(
    "Given ontology create Dictionary (phs_dictionary) and Snippets (snippets.cson) for Atom and PhenoScript.
    Install the Atom packages: r-syntax and snippet-injector.\n
Usage: snips.r infile dir -u\n
Options:\n
infile: input ontology\n
dir: output directory for phs_dictionary and snippets.cson\n
-u: update snippets and dictionary in Atom directory (should be specified in phs_Global_Args.txt) \n
"
  )
  quit()
}



#suppressPackageStartupMessages(library("dplyr"))

#---- Get local dir
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)

source(file.path(script.basename, "phsDictionary", "dependencies.R"))
#source(file.path(script.basename, "phsDictionary", "snips_functions.R"))

#---- Get local dir

# print(script.basename)
# print(file)
# print(file.out)
# print(update.arg)

#   ____________________________________________________________________________
#   Make Dictionary & Snippets for Atom                                     ####
onto.in <- file
dic.out <- file.path(file.out, 'phs_dictionary.csv')
snip.out <- file.path(file.out, 'snippets.cson')

if (!dir.exists(file.out)) {
  dir.create(file.out)
}

##  ............................................................................
##  Make Dictionary                                                         ####
make_dic <-paste0('./', file.path("phsDictionary", 'cmdPhsDic.R'), ' ', onto.in, ' ', dic.out )
system(make_dic)

##  ............................................................................
##  Make Snippets                                                           ####
make_snps <-paste0('./', file.path("phsDictionary", 'cmdSnips.R'), ' ', dic.out, ' ', snip.out )
system(make_snps)


##  ............................................................................
##  Update snippets in Atom directory                                       ####

if (!is.na(update.arg)){
  if (update.arg=='-u'){
    source(file.path(script.basename, "phs_Global_Args.txt"))
    cat('Updating snippets in Atom directory:\n')
    cat('\tCopying', dic.out, 'and', snip.out, 'to Atom at:\n')
    cat('\t\t', PATH_TO_ATOM, '\n')
    file.copy(from=dic.out, to=PATH_TO_ATOM, overwrite = T)
    file.copy(from=snip.out, to=PATH_TO_ATOM, overwrite = T)
    #print(PATH_TO_ATOM)
  }
}




