import codecs
from phenospy.snips_fun import *

# -----------------------------------------
# Read VScode snips in JSON and make dictionaries
# -----------------------------------------

# yaml_file = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phs-config.yaml'
# json_iri, json_type, json_lab = make_dicsFromSnips(yaml_file)
def make_dicsFromSnips(phs_yaml):
    # -----------------------------------------
    # Read configuration yaml
    # -----------------------------------------

    # print(f"{Fore.BLUE}Reading yaml file...{Style.RESET_ALL}")
    # with open(yaml_file, 'r') as f_yaml:
    #     phs_yaml = yaml.safe_load(f_yaml)
    # # print(phs_yaml)
    # print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

    # -----------------------------------------
    # Read JSON snippets
    # -----------------------------------------

    f_path = phs_yaml['snippet-dir']
    f_path = os.path.join(f_path, "phs-snippets.json")
    print(f"{Fore.BLUE}Reading snippets from JSON:{Style.RESET_ALL}", f_path)

    with codecs.open(f_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    # f = open(f_path)
    # json_file = json.load(f)
    # f.close()
    print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

    # for i in json_file:
    #     print(json_file[i]['prefix'])
    # ss= {}
    # ss.update({'ro-bearer_of': 'http://purl.obolibrary.org/obo/RO_0000053'})
    # ss.update({'>>': 'http://purl.obolibrary.org/obo/RO_0000053'})

    # -----------------------------------------
    # Double check if labels are unique
    # -----------------------------------------
    print(f"{Fore.BLUE}Checking if labels (label_4_translation) in snippets are unique...{Style.RESET_ALL}")
    # check duplicates
    label_phs = []
    for i in json_file:
        if (json_file[i]['type'] != 'Tmp'):
            label_phs.append(json_file[i]['label_4_translation'][0])
    #
    # label_phs.append('pato-swollen')
    unique_label_phs = set(label_phs)
    all_dupl = []
    if (len(label_phs) != len(unique_label_phs)):
        print(f"{Fore.RED}Warning! Some labels are duplicated! Fix it!{Style.RESET_ALL}")
        for unique_lab in unique_label_phs:
            # print(unique_lab)
            indeces = [index for index, element in enumerate(label_phs) if element == unique_lab]
            if (len(indeces) > 1):
                all_dupl.append(indeces)
        # i=499
        for dupl in all_dupl:
            for i in dupl:
                print(label_phs[i])
        exit()
    else:
        print(f"{Fore.GREEN}Good! All snippet labels are unique!{Style.RESET_ALL}")

    # -----------------------------------------
    # Make snippet dictionaries
    # -----------------------------------------

    json_iri = {}       # 'hao-annellus': 'http://purl.obolibrary.org/obo/HAO_0000095'
    json_type = {}      # 'http://purl.obolibrary.org/obo/HAO_0000097': 'C'
    json_lab = {}       # 'http://purl.obolibrary.org/obo/HAO_0000097': 'anteclypeus'
    for i in json_file:
        #print(json_file[i]['label_4_translation'])
        if (json_file[i]['type'] != 'Tmp'):
            lab = json_file[i]['label_4_translation']
            iri = json_file[i]['iri']
            lab_org = json_file[i]['label_original']
            type = json_file[i]['type']
            for la in lab:
                json_iri.update({la: iri})
            json_type.update({iri: type})
            if iri not in json_lab:
                json_lab.update({iri: lab_org})

    print(f"{Fore.GREEN}Good! Dictionaries from JSON snippets are constructed!{Style.RESET_ALL}")
    # json_iri['<']
    # json_iri['bfo-part_of']
    # json_type['http://purl.obolibrary.org/obo/BFO_0000050']
    # json_lab['http://purl.obolibrary.org/obo/BFO_0000050']
    return json_iri, json_type, json_lab


# dic_iri, dic_type, dic_lab = make_dicsFromSnips(yaml_file)
class snipsLabelDictionary:
    def __init__(self, dic_iri, dic_type, dic_lab):
        self.untranslated = []
        self.countNA = 0
        self.countLBS = 0
        self.dic_iri = dic_iri
        self.dic_type = dic_type
        self.dic_lab = dic_lab
        # dt = pd.read_csv(file)
        # key = pd.DataFrame(dt, columns=['IRI', 'label.final'])
        # ll = key.to_dict('records')
        # self.dd = {}
        # for i in ll:
        #     # print(i)
        #     # dd[i['IRI']]=i['label.nospace']
        #     self.dd[i['label.final']] = i['IRI']
    def resetCount(self):
        self.countNA = 0
        self.countLBS = 0
    def translate_lab(self, label):
        if label in self.dic_iri:
            self.countLBS += 1
            iri = self.dic_iri[label]
            lab_org = self.dic_lab[iri]
            type_snips = self.dic_type[iri]
            return iri, lab_org, type_snips
        else:
            self.countNA += 1
            self.untranslated.append(label)
            return 'NA', 'NA', 'NA'
    def print_untrans(self):
        self.untr = list(set(self.untranslated))
        self.untr.sort()
        # print('\t Untranslated terms:')
        # print(f"{Fore.RED}\nUntranslated terms:{Style.RESET_ALL}")
        for item in self.untr:
            print(f"{Fore.RED}\t%s{Style.RESET_ALL}" % item)
            #print('\t', item)
    def reset_untrans(self):
        self.untranslated = []