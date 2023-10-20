import xml.etree.ElementTree as ET


# tree = ET.ElementTree(ET.fromstring(out_xml))
# ET.register_namespace('phs', 'https://github.com/sergeitarasov/PhenoScript')
# root = tree.getroot()
# xml_add_YamlMeta(root, phs_yaml, base_iri)
def xml_add_YamlMeta(root, phs_yaml, base_iri):

    data = phs_yaml
    # create the root XML element
    meta = ET.Element("phs-config-yaml")

    # add the base-iri element
    iri_elem = ET.SubElement(meta, "base-iri")
    iri_elem.text = base_iri

    # add the authors element and its subelements
    authors = ET.SubElement(meta, "authors")
    for name, orcid in data["authors"].items():
        author = ET.SubElement(authors, "author")
        author.set("name", name)
        author.text = orcid
    
    # add project title
    project_title = ET.SubElement(meta, "project-title")
    project_title.text = data["project-title"]

    # add the importOntologies element and its subelements
    import_ontologies = ET.SubElement(meta, "importOntologies")
    for ontology in data["importOntologies"]:
        import_ontology = ET.SubElement(import_ontologies, "importOntology")
        import_ontology.text = ontology

    return root.insert(0, meta)





