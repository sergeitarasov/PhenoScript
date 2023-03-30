# former namespace_functions.py

import json
import os
from sys import exit

import yaml
from colorama import Fore, Style
from colorama import init as colorama_init
from owlready2 import *

# import importlib.resources as importlib_resources

colorama_init()
#print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")

#----


# returns Path to phenospy package
def get_phenospyPath():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

# iri = 'http://purl.obolibrary.org/obo/HAO_0000232'
# pref, trimmed_iri = getNamespace(iri, nmp_store)
def getNamespace(iri, nmp_store):
    for i in nmp_store:
        #print(i[2])
        spl = iri.split(i[2])
        #print(spl)
        if (len(spl) == 2) and (spl[0] == ''):
            return (i[1], spl[1])
    return (None, None)

# pref, trimmed_iri = getNamespace('http://purl.obolibrary.org/obo/IAO_8000011', nmp_store)
# snip = snippetInfo('C', 'this label', 'http://purl.obolibrary.org/obo/IAO_8000011', pref,  trimmed_iri)
# snip = snippetInfo('C', 'dd', 'http://purl.obolibrary.org/obo/IAO_8000011', 'Default',  trimmed_iri)
# print(snip)
# print(snip.printJson())
class snippetInfo:
    def __init__(self, type, label = None, iri = None, prefix = None, trimmed_iri = None, definition='', sep='-'):
        self.type = type
        self.label = label
        self.iri = iri
        self.prefix = prefix
        self.trimmed_iri = trimmed_iri
        self.label_phs = None
        # fixing defintion
        self.definition = definition
        self.definition =  self.definition.replace('\n', '  ')
        self.definition = self.definition.replace('\t', '  ')
        self.definition = self.definition.replace('"', "'")
        self.definition = '(' + self.type + '): ' + self.definition
        if (iri is None):
            print('iri  is absent')
        if  (label is None):
            self.label = trimmed_iri
        if (prefix is None):
            print('prefix is absent')
            self.prefix = 'NOPREF'
        self.label_phs = self.prefix + sep + self.label
        self.iri4snippet = self.prefix + sep + trimmed_iri
        if  (prefix == 'Default'):
            self.prefix = 'Default'
            self.label_phs = self.label
            self.iri4snippet = 'def' + sep +trimmed_iri
        self.label_phs = self.label_phs.replace(' ', '_')
        self.label_phs = self.label_phs.replace('/', '_')
        self.label_4_translation = self.label_phs
        self.label_no_ns = self.label.replace(' ', '_')
        #self.label_no_ns = self.label_phs
        if (type == 'OP') or (type == 'DP') or (type == 'AP'):
            self.label_phs = '.' + self.label_phs
    def printJson(self):
        out = \
        '"(%s) %s": {\n' \
        '"prefix": ["%s"],\n' \
        '"body": ["%s"],\n' \
        '"description": "%s",\n' \
        '"iri": "%s",\n' \
        '"label_4_translation": ["%s"],\n' \
        '"label_original": "%s",\n' \
        '"type": "%s"\n' \
        '}' % (self.type, self.iri4snippet, self.label_phs, self.label_phs, self.definition, self.iri, \
            self.label_4_translation, self.label, self.type)
        return str(out)
    def __repr__(self):
        ret = 'type: ' + str(self.type) + '\n' +\
            '\t original label: ' + str(self.label) + '\n' + \
            '\t label phs-no-ns: ' + str(self.label_no_ns) + '\n' + \
            '\t label phs: ' + str(self.label_phs)  + '\n' + \
            '\t label 4 translation: ' + str(self.label_4_translation) + '\n' + \
            '\t iri: ' + str(self.iri) + '\n' + \
            '\t namespace pref: ' + str(self.prefix) + '\n' +\
            '\t trimmed_iri: ' + str(self.trimmed_iri)  + '\n' +\
            '\t definition: ' + str(self.definition) + '\n' + \
            '\t iri 4 snippet: ' + str(self.iri4snippet) + '\n'
        return str(ret)

# yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/src/reasoning/phs-config.yaml'
# printUniqueIRIs(yaml_file)
def printUniqueIRIs(yaml_file):
    # -----------------------------------------
    # Read configuration yaml
    # -----------------------------------------
    print(f"{Fore.BLUE}Reading yaml file...{Style.RESET_ALL}")
    with open(yaml_file, 'r') as f_yaml:
        phs_yaml = yaml.safe_load(f_yaml)
    # print(phs_yaml)
    print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")
    #
    # -----------------------------------------
    # Processing ontologies
    # -----------------------------------------
    print(f"{Fore.BLUE}Start reading ontologies...{Style.RESET_ALL}")
    # get ontologies from yaml
    onto_store = phs_yaml['importOntologies']
    # keep all snips here:
    iris_underscore = []
    iris_hash = []
    for onto_path in onto_store:
        # print(onto_path)
        print(f"\n\t{Fore.BLUE}Loading ontology:{Style.RESET_ALL}", onto_path)
        try:
            onto = get_ontology(onto_path).load()
        except:
            onto = get_ontology(onto_path).load()
        obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
        print(f"\t\t{Fore.GREEN}The ontology loaded!{Style.RESET_ALL}")
        # --------------
        # Classes (C)
        # --------------
        # x = 'http://purl.obolibrary.org/obo/pato#increased_in_magnitude_relative_to'
        # x.split('_')

        print(f"\t{Fore.BLUE}Extracting IRIs...{Style.RESET_ALL}")
        #
        onto_obj = onto.classes()
        for item in onto_obj:
            i = item.iri.split('_')[0]
            iris_underscore.append(i)
            if '#' in item.iri:
                i = item.iri.split('#')[0]
                iris_hash.append(i)

        # --------------
        # OP
        # --------------
        onto_obj = onto.object_properties()
        for item in onto_obj:
            i = item.iri.split('_')[0]
            iris_underscore.append(i)
            if '#' in item.iri:
                i = item.iri.split('#')[0]
                iris_hash.append(i)
        # --------------
        # DP
        # --------------
        onto_obj = onto.data_properties()
        for item in onto_obj:
            i = item.iri.split('_')[0]
            iris_underscore.append(i)
            if '#' in item.iri:
                i = item.iri.split('#')[0]
                iris_hash.append(i)
        # --------------
        # AP
        # --------------
        onto_obj = onto.annotation_properties()
        for item in onto_obj:
            i = item.iri.split('_')[0]
            iris_underscore.append(i)
            if '#' in item.iri:
                i = item.iri.split('#')[0]
                iris_hash.append(i)
        #
        print(f"\t{Fore.GREEN}IRIs extracted!\n{Style.RESET_ALL}")
    #
    unique_underscore = set(iris_underscore)
    unique_hash = set(iris_hash)
    print(f"\t{Fore.RED}\nUnique IRIs split with '_':{Style.RESET_ALL}")
    print(*sorted(unique_underscore), sep='\n')
    print(f"\t{Fore.RED}\nUnique IRIs split with '#':{Style.RESET_ALL}")
    print(*sorted(unique_hash), sep ='\n')
#


