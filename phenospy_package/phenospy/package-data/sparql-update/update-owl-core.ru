PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX phs: <https://github.com/sergeitarasov/PhenoScript/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>


# This file contains SPARQL queries to convert graph patterns 
# written in Phenoscript as Abox into some other statements (e.g., classes)

# ------------------------------------------------------------------
# Cardinality Restrictions:
#
# aism-setose_cuticle > aism-cuticular_seta .phs-has_element_count 3;
# ------------------------------------------------------------------
#
# In OWL, cardinality must always be defined over an object property.
# It is NOT valid to state "exactly 2 leg" without specifying a relation.
#
# Correct pattern:
#   We must have a class e.g,  'has_component exactly 2 leg'
#
# This is expressed as an OWL restriction:
#   _:r rdf:type owl:Restriction ;
#       owl:onProperty obo:RO_0002180 ;          # has_component
#       owl:qualifiedCardinality "2"^^xsd:nonNegativeInteger ;
#       owl:onClass obo:AISM_0000039 .           # seta
#
# Semantics:
#   The subject individual belongs to a class that has exactly 2 distinct components
#   that are instances of the class 'leg'.
#
# Phenoscript pattern:
# aism-setose_cuticle > aism-cuticular_seta .phs-has_element_count 3;
#
# OWL pattern;
# aism-setose_cuticle rdf:type (has_component exactly 3 aism-cuticular_seta)
#
# Therefore, we transform count-based patterns into
# OWL cardinality restrictions using SPARQL.
#
# This transformation:
#   1. Reads the count value (data property)
#   2. Retrieves the class of the component
#   3. Creates an owl:Restriction blank node
#   4. Attaches it via rdf:type to the subject
#   5. Removes the original scaffold individuals
#
#
# SPARQL specification:
#
# aism-setose_cuticle > aism-cuticular_seta .phs-has_element_count 3;
#    col (collection)   comp (component)            count
# Terms:
# [setose cuticle](http://purl.obolibrary.org/obo/AISM_0000530)
# [has member](http://purl.obolibrary.org/obo/RO_0002351)
# [has element count](https://github.com/sergeitarasov/PhenoScript/PHS_0000016)
# [has part](http://purl.obolibrary.org/obo/BFO_0000051)
# [cuticular seta](http://purl.obolibrary.org/obo/AISM_0000039)
# [has component](http://purl.obolibrary.org/obo/RO_0002180)
# [phs_original_assertion](https://github.com/sergeitarasov/PhenoScript/PHS_0000005)
# [phs_original_class](https://github.com/sergeitarasov/PhenoScript/PHS_0000002)
#
# ------------------------------------------------------------------

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
  ?col obo:BFO_0000051 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000002> ?compClass .

  BIND(BNODE() AS ?restr)
  BIND(STRDT(STR(?count), xsd:nonNegativeInteger) AS ?convertedCount)
};


# Delete annotation Axioms for triples that have edges: PHS_0000016 or BFO_0000051
# without deleting triple annotations we cannot remove the corresponding individuals
# <owl:Axiom>
#   <owl:annotatedSource: N1
#   <owl:annotatedProperty: has_part
#   <owl:annotatedTarget: N2 or Number (3)
#   phs_original_assertion (PHS_0000005): true
# </owl:Axiom>
#
# We have two two triples in:
#  aism-setose_cuticle > aism-cuticular_seta .phs-has_element_count 3;
#    col (collection)   comp (component)            count
# 
# Annotations should be deleted from each of them:
# - aism-setose_cuticle > aism-cuticular_seta
# - aism-cuticular_seta .phs-has_element_count 3

# Delete annotation Axioms from:  aism-cuticular_seta .phs-has_element_count 3
DELETE {
  ?axiom ?p ?o .
}
WHERE {
  ?col obo:BFO_0000051 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .

  ?axiom rdf:type owl:Axiom ;
         owl:annotatedSource ?comp ;
         owl:annotatedProperty <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ;
         owl:annotatedTarget ?count ;
         ?p ?o .
};

# Delete annotation Axioms from: aism-setose_cuticle > aism-cuticular_seta
DELETE {
  ?axiom ?p ?o .
}
WHERE {
  ?col obo:BFO_0000051 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .

  ?axiom rdf:type owl:Axiom ;
         owl:annotatedSource ?col ;
         owl:annotatedProperty obo:BFO_0000051 ;
         owl:annotatedTarget ?comp ;
         ?p ?o .
};


# Delete the component individual and leave the collection individual
DELETE {
  ?col obo:BFO_0000051 ?comp .
  ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
  ?comp ?prop ?extraTarget .
}
WHERE {
  ?col rdf:type owl:NamedIndividual .
   ?col obo:BFO_0000051 ?comp .
   ?comp <https://github.com/sergeitarasov/PhenoScript/PHS_0000016> ?count .
   ?comp ?prop ?extraTarget .
};


# ------------------------------------------------------------------
# Others
# ------------------------------------------------------------------