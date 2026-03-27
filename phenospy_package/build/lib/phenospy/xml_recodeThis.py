import xml.etree.ElementTree as ET

# -----------------------------------------
# Recoding 'this' keyword to respective nodes 
# -----------------------------------------

def xmlRecodeThis(root, ns):
    phs = '{https://github.com/sergeitarasov/PhenoScript}'
    # make mapping to extract parents quickly
    parent_map = {c:p for p in root.iter() for c in p}
    OTUs=root.findall(".//phs:otu_object", ns)
    for otu in OTUs:
        this_node=otu.find(".//phs:otu_properties//phs:node_property[@phs:var-iri='KeyWord:this'][@phs:value-iri='KeyWord:True']", ns)
        # print('THIS:', this_node)
        if this_node is not None:
            this_parent = parent_map[this_node]
            # <phs:node phs:node_id="https://urn:uuid:8f7fbcbc-ccbb-11ed-beb4-acde48001122/id-4e3742" phs:triple_pos="3" phs:node_name="hao-female_organism" 
            # phs:fromNegativeEdge="False" phs:iri="http://purl.obolibrary.org/obo/HAO_0000028" phs:label_original="female organism" phs:type_onto="C">
            p_node_id         = this_parent.get(phs+'node_id')
            p_node_name       = this_parent.get(phs+'node_name')
            p_iri             = this_parent.get(phs+'iri')
            p_label_original  = this_parent.get(phs+'label_original')
            p_type_onto       = this_parent.get(phs+'type_onto')
            #
            ophuList = otu.find(".//phs:ophu_list", ns)
            this_ophuNodes = ophuList.findall(".//phs:node[@phs:iri='KeyWord:this']", ns)
            for this in this_ophuNodes:
                this.set('{https://github.com/sergeitarasov/PhenoScript}node_id', p_node_id)
                this.set('{https://github.com/sergeitarasov/PhenoScript}node_name', p_node_name)
                this.set('{https://github.com/sergeitarasov/PhenoScript}iri', p_iri)
                this.set('{https://github.com/sergeitarasov/PhenoScript}label_original', p_label_original)
                this.set('{https://github.com/sergeitarasov/PhenoScript}type_onto', p_type_onto)
                # this.text 

# Save
# Create an ElementTree object from the root element
# tree_save = ET.ElementTree(root)
# # Save the XML tree to a file
# xml_save = '/Users/taravser/Documents/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data' \
#            '/phs_xml.xml'
# tree_save.write(xml_save, encoding="utf-8", xml_declaration=True)