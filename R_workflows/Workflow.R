#---------------------------------------
#
# This is the workflow that translates
#  Phenoscript into OWL for Gryonoides
#
# author: Sergei Tarasov
#
#---------------------------------------

library(reticulate)
library(dplyr)

#   ____________________________________________________________________________
#   Get ontologies                                                          ####


# Ontologies
ontos <- c(
#'https://raw.githubusercontent.com/hymao/hao/master/hao.owl',
#'http://purl.obolibrary.org/obo/aism.owl', # use local version 'cuticle of protibia'
'https://raw.githubusercontent.com/insect-morphology/colao/master/colao.owl',
'https://raw.githubusercontent.com/pato-ontology/pato/master/pato.owl',
'https://raw.githubusercontent.com/obophenotype/biological-spatial-ontology/master/bspo.owl',
'https://raw.githubusercontent.com/evoinfo/cdao/master/cdao.owl',
'https://raw.githubusercontent.com/information-artifact-ontology/IAO/v2020-12-09/iao.owl',
'https://raw.githubusercontent.com/oborel/obo-relations/master/ro.owl'
)

ontos <- c(
  #'https://raw.githubusercontent.com/hymao/hao/master/hao.owl',
  'http://purl.obolibrary.org/obo/aism.owl' # use local version 'cuticle of protibia')

# Download
#'curl -LJO https://raw.githubusercontent.com/insect-morphology/colao/master/colao.owl'
down <- paste0('-LJO ', ontos, collapse = ' ') %>% paste0('curl ', .)
setwd('data/ontologies')
system(down)

# Merge using ROBOT
#robot merge --inputs "edit*.owl" --output results/merged2.owl
system('robot merge --inputs "*.owl" --output colao_merged.owl')
setwd('../'); setwd('../')
getwd()

setwd('data/ontologies')
system('robot merge --input aism.owl --input pato.owl --input bspo.owl --output ais-pato_merged.owl')

system('robot merge --input aism.owl --input bspo.owl --output ais-pato_merged.owl')

system('robot merge --input colao.owl --input ro.owl --input bspo.owl --output ais-pato_merged.owl')

setwd('../'); setwd('../')
#   ____________________________________________________________________________
#   Input and Output                                                        ####

# Input
dic.path.in <- 'phsDictionary'
data.path.in <- 'data'
onto.in <- file.path(data.path.in, 'ontologies/colao_merged.owl')
#phs.file.in <- file.path(data.path.in, 'test.phs')
phs.file.in <- file.path(data.path.in, 'phs/colao_AP.phs')

# Output
results.out <- 'results'
dic.path.out <- 'results/dictionary'
#dic.out <- file.path(dic.path.out, 'Gryo_dic.csv')
dic.out <- file.path(dic.path.out, 'dictionary.csv')
#xml.out <- file.path(results.out, 'phs_colao.xml')
xml.out <- file.path(results.out, 'phs_colao_AP.xml')
instance_IRI='https://orcid.org/0000-0001-5237-2330/'

#   ____________________________________________________________________________
#   Check if Reasoning is possible                                         ####

robot reason --reasoner ELK \
--input ais-pato_merged.owl \
-D debug.owl

robot reason --reasoner ELK \
--input colao_merged.owl \
-D debug.owl

#   ____________________________________________________________________________
#   Make Dictionary & Snippets for Atom                                     ####

##  ............................................................................
##  Make Dictionary                                                         ####
make_dic <-paste0('./', file.path(dic.path.in, 'cmdPhsDic.R'), ' ', onto.in, ' ', dic.out )
system(make_dic)

##  ............................................................................
##  Make Snippets                                                           ####
make_snps <-paste0('./', file.path(dic.path.in, 'cmdSnips.R'), ' ', dic.out, ' ', 'results/dictionary/snippets.cson' )
system(make_snps)

##  ............................................................................
##  Update Snippets in Atom dir
atom.path='/Users/taravser/.atom'
file.copy(from='results/dictionary/snippets.cson', to=atom.path, overwrite = T)
file.copy(from='results/dictionary/dictionary.csv', to=atom.path, overwrite = T)

#   ____________________________________________________________________________
#   PhenoScript to XML                                                      ####

py_run_file("src/phs_init.py")

pyPhenoScriptToXML <- sprintf("PhenoScriptToXML(file_phs='%s', file_phsDic='%s', xml_out='%s', instance_IRI='%s')",
                                               phs.file.in, dic.out, xml.out, instance_IRI)

# !!! For manual parsing see src/phs_manual_parse.py
py_run_string(pyPhenoScriptToXML)



#   ____________________________________________________________________________
#   Compile: PhenoScript XML into OWL                                       ####

library(xml2)
source('R/write_xml.R')

# Namespace for XML to OWL
gryo.namespace =c('obo'="http://purl.obolibrary.org/obo/",
                  rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                  'owl'="http://www.w3.org/2002/07/owl#",
                  rdfs="http://www.w3.org/2000/01/rdf-schema#",
                  sta ="https://orcid.org/0000-0001-5237-2330/",
                  'oboI'="http://www.geneontology.org/formats/oboInOwl#",
                  'newT'="http://github.com/sergeitarasov/PhenoScript/gryo/",
                  'pato'="http://purl.obolibrary.org/obo/pato#"
)



# let's read xml PhS: xml.out
phs <- read_xml(xml.out)
print(phs)

# Now compiling xml PhS into OWL
PhenoScriptToOWL(PS=phs, phs.namespace=gryo.namespace, onto.in,
                 xml_instances.out='results/Gryo_only_instances.owl', file.out='results/phsGryo_merged.owl')
