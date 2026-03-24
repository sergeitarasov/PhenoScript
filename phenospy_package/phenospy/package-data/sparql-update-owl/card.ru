PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX phs: <https://github.com/sergeitarasov/PhenoScript/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# Convert individual based expression to cardinality Restriction: has_component exactly N Components.

# bash
# update --data phs.ttl --update card.ru --dump > out.ttl

# Suppose we have the following statement:
# bspo-anterior_region >  aism-setose_cuticle .ro-has_member aism-cuticular_seta .phs-has_element_count 2;
# where                   col (collection)                   comp (component)                          count

# !!! Remeber to change .ro-has_member and .phs-has_element_count Everywhere

# Terms:
# [setose cuticle](http://purl.obolibrary.org/obo/AISM_0000530)
# [has member](http://purl.obolibrary.org/obo/RO_0002351)
# [has element count](https://github.com/sergeitarasov/PhenoScript/PHS_0000016)
# [has part](http://purl.obolibrary.org/obo/BFO_0000051)
# [cuticular seta](http://purl.obolibrary.org/obo/AISM_0000039)
# [has component](http://purl.obolibrary.org/obo/RO_0002180)
# [phs_original_assertion](https://github.com/sergeitarasov/PhenoScript/PHS_0000005)
# [phs_original_class](https://github.com/sergeitarasov/PhenoScript/PHS_0000002)

# Insert has_component term if it does not exist
INSERT {
  obo:RO_0002180 a owl:ObjectProperty ;
                  rdfs:label "has component" .
}
WHERE {
  FILTER NOT EXISTS {
    obo:RO_0002180 a owl:ObjectProperty .
  }
};


INSERT {
  ?col rdf:type ?restr .
  ?restr rdf:type owl:Restriction .
  ?restr owl:onProperty obo:RO_0002180 .
  ?restr owl:qualifiedCardinality ?convertedCount .
  ?restr owl:onClass ?compClass .
}
WHERE {
  ?col rdf:type owl:NamedIndividual .
  ?col obo:RO_0002351 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000002> ?compClass .

  BIND(BNODE() AS ?restr)
  BIND(STRDT(STR(?count), xsd:nonNegativeInteger) AS ?convertedCount)
};


# Delete annotation Axioms for triples that have edges: PHS_0000016 or RO_0002351
# without deleting triple annotations we cannot remove the corresponding individuals
DELETE {
  ?axiom rdf:type owl:Axiom ;
         owl:annotatedSource ?source ;
         owl:annotatedProperty ?property ;
         owl:annotatedTarget ?target ;
         ?extraProperty ?extraValue .
}
WHERE {
  ?axiom rdf:type owl:Axiom ;
         owl:annotatedSource ?source ;
         owl:annotatedProperty ?property ;
         owl:annotatedTarget ?target ;
         ?extraProperty ?extraValue .
  FILTER(?property = <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> || ?property = obo:RO_0002351)
};


# Delete the component individual and leave the collection individual
DELETE {
  ?col obo:RO_0002351 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
  ?comp ?prop ?extraTarget .
}
WHERE {
  ?col rdf:type owl:NamedIndividual .
   ?col obo:RO_0002351 ?comp .
   ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
   ?comp ?prop ?extraTarget .
};
