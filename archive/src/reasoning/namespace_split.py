# my functions
from namespace_functions import *



# -----------------------------------------
# Arguments
# -----------------------------------------

yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/src/reasoning/phs-config.yaml'

# -----------------------------------------
# Read configuration yaml
# -----------------------------------------

print(f"{Fore.BLUE}Reading yaml file...{Style.RESET_ALL}")
with open(yaml_file, 'r') as f_yaml:
    phs_yaml = yaml.safe_load(f_yaml)
#print(phs_yaml)
print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

# -----------------------------------------
# Processing yaml namespace
# ----------------------------------------

nmp_store=[]
nmp = phs_yaml['namespace']['others']
for key in nmp:
    # [IRI length, prefix, IRI, is.default.namespace]
    x = [len(nmp[key]), key, nmp[key], False ]
    nmp_store.append(x)
    #print(x)

# add default
deff = phs_yaml['namespace']['default']
nmp_store.append([len(deff), 'Default', deff, True ])
nmp_store.sort(reverse=True)

print(f"{Fore.GREEN}Good! Yaml namespace is processed!{Style.RESET_ALL}")

# -----------------------------------------
# Check if namespace has unique elements
# -----------------------------------------
prefs = [i[1] for i in nmp_store]
iris = [i[2] for i in nmp_store]

dupl = set([x for x in prefs if prefs.count(x) > 1])
if len(dupl)>0:
    print(f"{Fore.RED}Warning! Yaml contains  duplicated namespace prefixes. Fix it!{Style.RESET_ALL}")
    exit()
dupl = set([x for x in iris if iris.count(x) > 1])
if len(dupl)>0:
    print(f"{Fore.RED}Warning! Yaml contains  duplicated namespace IRIs. Fix it!{Style.RESET_ALL}")
    exit()

# -----------------------------------------
# Processing ontologies
# -----------------------------------------

# def render_using_label(entity):
#     return entity.label.first() or entity.name
#
# set_render_func(render_using_label)
# set_log_level(9)

print(f"{Fore.BLUE}Start reading ontologies...{Style.RESET_ALL}")

# get ontologies from yaml
onto_store = phs_yaml['importOntologies']
# keep all snips here:
snips = []
for onto_path in onto_store:
    # print(onto_path)
    print(f"\n\t{Fore.BLUE}Loading ontology:{Style.RESET_ALL}", onto_path)
    try:
        onto = get_ontology(onto_path).load()
    except:
        onto = get_ontology(onto_path).load()
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    print(f"\t\t{Fore.GREEN}The ontology loaded!{Style.RESET_ALL}")
    # -----------------------------------------
    # Making snippets
    # -----------------------------------------
    # --------------
    # Classes (C)
    # --------------
    print(f"\t{Fore.BLUE}Extracting snippets...{Style.RESET_ALL}")
    #
    onto_obj = onto.classes()
    for item in onto_obj:
        # print(item.iri)
        # print(item.IAO_0000115.first()) # defintion
        #print(item, item.iri, getNamespace(item.iri, nmp_store))
        pref, trimmed_iri = getNamespace(item.iri, nmp_store)
        if (pref is not None) and (trimmed_iri is not None):
            try:
                defin = item.IAO_0000115.first()
            except:
                defin = ''
            if defin is None:
                defin=''
            snip = snippetInfo('C', item.label.first(), item.iri, pref, trimmed_iri, defin)
            snips.append(snip)
            #print(snip)
        else:
            print(f"\t\t\t{Fore.RED}Warning! See phs-config.yaml. Namespace is not defined for{Style.RESET_ALL}{Fore.BLUE}", item, item.iri)
    # --------------
    # OP
    # --------------
    onto_obj = onto.object_properties()
    for item in onto_obj:
        #print(item.iri)
        # print(item.IAO_0000115.first()) # defintion
        #print(item, item.iri, getNamespace(item.iri, nmp_store))
        pref, trimmed_iri = getNamespace(item.iri, nmp_store)
        if (pref is not None) and (trimmed_iri is not None):
            defin = item.IAO_0000115.first()
            if defin is None:
                defin=''
            snip = snippetInfo('OP', item.label.first(), item.iri, pref, trimmed_iri, defin)
            snips.append(snip)
            #print(snip)
        else:
            print(f"\t\t\t{Fore.RED}Warning! See phs-config.yaml. Namespace is not defined for{Style.RESET_ALL}{Fore.BLUE}", item, item.iri)
    # --------------
    # DP
    # --------------
    onto_obj = onto.data_properties()
    for item in onto_obj:
        pref, trimmed_iri = getNamespace(item.iri, nmp_store)
        if (pref is not None) and (trimmed_iri is not None):
            defin = item.IAO_0000115.first()
            if defin is None:
                defin=''
            snip = snippetInfo('DP', item.label.first(), item.iri, pref, trimmed_iri, defin)
            snips.append(snip)
            #print(snip)
        else:
            print(f"\t\t\t{Fore.RED}Warning! See phs-config.yaml. Namespace is not defined for{Style.RESET_ALL}{Fore.BLUE}", item, item.iri)
    # --------------
    # AP
    # --------------
    onto_obj = onto.annotation_properties()
    for item in onto_obj:
        pref, trimmed_iri = getNamespace(item.iri, nmp_store)
        if (pref is not None) and (trimmed_iri is not None):
            defin = item.IAO_0000115.first()
            if defin is None:
                defin=''
            snip = snippetInfo('AP', item.label.first(), item.iri, pref, trimmed_iri, defin)
            snips.append(snip)
            #print(snip)
        else:
            print(f"\t\t\t{Fore.RED}Warning! See phs-config.yaml. Namespace is not defined for{Style.RESET_ALL}{Fore.BLUE}", item, item.iri)
    #
    print(f"\t{Fore.GREEN}The snippets extracted!\n{Style.RESET_ALL}")

#len(snips)


# -----------------------------------------
# Select Unique IRIs
# -----------------------------------------

# get all iris from snips
iris_phs=[]
for snip in snips:
    #print(snip.label_phs)
    iris_phs.append(snip.iri)

# select indices of unique iris
iri_index = list(set(i for i, x in enumerate(iris_phs) if x not in iris_phs[:i]))
# select unique snips based on the iri indeces
snips=[snips[i] for i in iri_index]

iris_phs=[]
for snip in snips:
    #print(snip.label_phs)
    iris_phs.append(snip.iri)

if len(iris_phs) == len(set(iris_phs)):
    print(f"\t{Fore.GREEN}Good! All snippet IRIs are unique!{Style.RESET_ALL}")
    print(f"\t{Fore.GREEN}Number of unique snippet IRIs is:{Style.RESET_ALL}", len(iris_phs))
else:
    print(f"\t{Fore.GREEN}Warning! The snippet IRIs contain duplicates! Fix it!\n{Style.RESET_ALL}")
    exit()

# -----------------------------------------
# Duplicated snippet labels
# -----------------------------------------

# check duplicates
label_phs=[]
for snip in snips:
    #print(snip.label_phs)
    label_phs.append(snip.label_4_translation)

unique_label_phs = set(label_phs)
all_dupl=[]
if (len(label_phs) != len(unique_label_phs)):
    print(f"{Fore.RED}Warning! Some labels are duplicated! {Style.RESET_ALL}")
    print(f"{Fore.BLUE}Resolving duplicated labels! For each duplicate adding <label>_IRI ...{Style.RESET_ALL}")
    for unique_lab in unique_label_phs:
        # print(unique_lab)
        indeces = [index for index, element in enumerate(label_phs) if element == unique_lab]
        if (len(indeces) > 1):
            all_dupl.append(indeces)
    # i=499
    for dupl in all_dupl:
        for i in dupl:
            snips[i].label_phs = snips[i].label_phs + '_' + snips[i].trimmed_iri
            snips[i].label_4_translation = snips[i].label_4_translation + '_' + snips[i].trimmed_iri
            snips[i].label_no_ns = snips[i].label_no_ns + '_' + snips[i].trimmed_iri
    print(f"{Fore.GREEN}Good! All labels are unique!{Style.RESET_ALL}")
else:
    print(f"{Fore.GREEN}Good! All labels are unique!{Style.RESET_ALL}")


# -----------------------------------------
# Check if snippets contains prohibited characters
# -----------------------------------------


# check if snippets contains prohibited characters
for snip in snips:
    #print(snip)
    x = snip.label_phs
    if ('#' in x) or ('/' in x):
        print(f"{Fore.RED}Warning! The snippet contains prohibited characters: #. Fix it! {Style.RESET_ALL}")
        print(snip)




# len(snips)
# print(snips[2285].printJson())
# print(snips[6490].printJson())


snips_json = ",\n".join([snip.printJson() for snip in snips])
snips_json = '{\n' + snips_json + '\n}'
#snips_json = { snips_json }
print(snips_json)

#print(json.dumps(snips_json))

with  open('/Users/taravser/Documents/Soft/VS_code_test/phenoscript/snippets/phs-snippets.json', 'w') as f:
    f.write(snips_json)
    f.close()

# read json
import json

f = open('/Users/taravser/Documents/Soft/VS_code_test/phenoscript/snippets/phs-snippets.json')
json_file = json.load(f)
f.close()


for i in json_file:
    print(json_file[i]['prefix'])


ss= {}
ss.update({'ro-bearer_of': 'http://purl.obolibrary.org/obo/RO_0000053'})
ss.update({'>>': 'http://purl.obolibrary.org/obo/RO_0000053'})


json_iri = {}
json_type = {}
json_lab = {}
for i in json_file:
    #print(json_file[i]['label_4_translation'])
    lab = json_file[i]['label_4_translation']
    iri = json_file[i]['iri']
    lab_org = json_file[i]['label_original']
    type = json_file[i]['type']
    for la in lab:
        json_iri.update({la: iri})
    json_type.update({iri: type})
    json_lab.update({iri: lab_org})

json_file['(OP) ro-0000053']
json_iri['>>']