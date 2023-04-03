import xml.etree.ElementTree as ET
from owlready2 import *
import uuid
import types

#-----------------------
# Arguments
#-----------------------

ontoPath = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/data'
ontoFile = 'colao_merged.owl'
phenex_XML='/Users/taravser/Documents/My_papers/Phenex_Coleo/Jennifer/BTOL_small.xml'

#--- Read in Ontology
set_log_level(9)
onto_path.append(ontoPath)
onto = get_ontology(ontoFile)
onto.load(reload_if_newer=True)
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
inf=onto.get_namespace("https://github.com/sergeitarasov/PhenoScript/inference/")

#-----------------------
# Functions
#-----------------------
# some previous functions:
# nodeIdGenerator(prefix='_ophu_', starting_id=1)
path_src="./src/"
exec(open(path_src+"phs_xml.py").read())

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)

# ----

tree = ET.parse(phenex_XML)
root = tree.getroot()

#xmlns="http://www.nexml.org/2009"
#xmlns:phen="http://www.bioontologies.org/obd/schema/pheno"
# additional (default) Args
phen='{http://www.bioontologies.org/obd/schema/pheno}'
nexml='{http://www.nexml.org/2009}'
ns = {'phen': 'http://www.bioontologies.org/obd/schema/pheno',
      'nexml': 'http://www.nexml.org/2009'
      }


#  <phen:typeref about="AISM:0000019" />
root.find(".//phen:typeref[@about='AISM:0000019']", ns)

for states in root.iter(nexml + 'states'):
    #print(states)
    for state in states.iter(nexml + 'state'):
        #print(state)
        state_label=state.get('label')
        print('STATE:', state_label)
        entity = state.find(".//phen:bearer", ns)
        #print('\t Entity:', entity)
        if entity is not None:
            entity_iri = entity.find(".//phen:typeref", ns).get('about')
            print('\t Entity:', entity_iri)
            qualifier = entity.find(".//phen:qualifier", ns)
            if qualifier is not None:
                qualifier_iri = qualifier.get('relation')
                print('\t Qualifier:', qualifier_iri )



#node = root.find(".//phen:typeref[@about='BSPO:0000028']", ns)
#getPostComposition(node)

# ---  Create Indv
node = root.find(".//phen:typeref[@about='BSPO:0000028']", ns)
UUID = str(uuid.uuid1())
entity_txt = 'obo.' + node.get('about').replace(':', '_')
N1 = eval(entity_txt + '(UUID)')
N1.label = IRIS[eval(entity_txt + '.iri')].label.first()
getPostComposition(node, N1)
def getPostComposition(node, N1):
    if node is not None:
        edge = node.find(".//phen:qualifier", ns)
        if edge is not None:
            node2 = edge.find(".//phen:typeref", ns)
            print(node.get('about'))
            print(edge.get('relation'))
            print(node2.get('about'))
            # ---  Create Indv
            UUID = str(uuid.uuid1())
            entity_txt = 'obo.' + node2.get('about').replace(':', '_')
            N2 = eval(entity_txt + '(UUID)')
            N2.label = IRIS[eval(entity_txt + '.iri')].label.first() + nid.makeId()
            #
            edge_txt = 'obo.' + edge.get('relation').replace(':', '_')
            Ed = IRIS[eval(edge_txt  + '.iri')]
            exec('N1.%s.append(N2)' % Ed.name)
            # ---
            getPostComposition(node2, N2)

for states in root.iter(nexml + 'states'):
    #print(states)
    for state in states.iter(nexml + 'state'):
        #print(state)
        state_label=state.get('label')
        print('STATE:', state_label)
        entity = state.find(".//phen:bearer", ns)
        #print('\t Entity:', entity)
        if entity is not None:
            node = entity.find(".//phen:typeref", ns)
            getPostComposition(node)


# obo.IAO_0000219 denotes
# obo.CDAO_0000138 TU
# obo.UBERON_0000468 multicellurlar organism
# obo.BFO_0000051 has part

global nid
nid = nodeIdGenerator(prefix='_', starting_id=1)
# nid.makeId()

# Loop over OTUs
for otu in root.iter(nexml + 'otu'):
    #print(otu)
    href = otu.find(".//nexml:meta[@href]", ns).get('href')
    print(otu.get('id'), otu.get('label'), href)
    # ---- make Taxon Class and Individual
    with obo:
        TaxonClass = types.new_class('tmp', (owl.Thing,))
    TaxonClass.label = otu.get('label')
    TaxonClass.iri = href
    UUID = str(uuid.uuid1())
    TaxonIndv = TaxonClass('https://temp/tmp' + UUID)
    TaxonIndv.label = 'DET_' + otu.get('label')
    # ---- Make and Link otu (TU) individual
    UUID = str(uuid.uuid1())
    OtuIndv = obo.CDAO_0000138('https://temp/tmp')
    # OtuIndv.iri = 'https://temp/tmp1' # this works
    # OtuIndv.iri = 'urn:uri:' + UUID # this does not work
    OtuIndv.iri = 'https://' + UUID
    OtuIndv.label = 'OTU_' + otu.get('label')
    OtuIndv.IAO_0000219.append(TaxonIndv)
    # ----
    matrix_row = root.find(".//nexml:row[@otu='%s']" % otu.get('id'), ns)
    for cell in matrix_row.iter(nexml + 'cell'):
        #print(cell)
        cell_state = cell.get('state')
        print(cell_state)
        # cell_state = 'state1483'
        # cell_state = 'state1491'
        state = root.find(".//nexml:state[@id='%s']" % cell_state, ns)
        if (state.get('label') == 'inapplicable'):
            print('inapplicable char')
        elif (state.get('label') == 'unknown'):
            print('unknown char')
        else:
            # some defines character character
            # identify type by quality
            if (state.find(".//phen:quality/phen:related_entity", ns) is not None):
                print('related_entity char')
                # if (state.find(".//phen:quality/phen:measurement", ns) is not None):
                    # print(measurement char)
            else:
                print('pure quality char')
                # --- find state bearer
                bearer = state.find(".//phen:bearer", ns)
                # --- Create unnique organisms for each character state for given TU
                UUID = str(uuid.uuid1())
                OrganismIndv = obo.UBERON_0000468(UUID)
                OrganismIndv.label = obo.UBERON_0000468.label.first() + nid.makeId()
                OtuIndv.IAO_0000219.append(OrganismIndv)
                # ---  Link Otu and state
                node = bearer.find(".//phen:typeref", ns)
                UUID = str(uuid.uuid1())
                entity_txt = 'obo.' + node.get('about').replace(':', '_')
                N1 = eval(entity_txt + '(UUID)')
                N1.label = IRIS[eval(entity_txt + '.iri')].label.first() + nid.makeId()
                OrganismIndv.BFO_0000051.append(N1)
                getPostComposition(node, N1)




outputFile = '/Users/taravser/Documents/My_papers/Phenex_Coleo/Jennifer/BTOL_small.owl'
onto.save(file = outputFile, format = "rdfxml")

print('\n DONE!!!\n')