PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX phs: <https://github.com/sergeitarasov/PhenoScript/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>


# This file contains SPARQL queries to prepare graph patterns 
# to be converted into natural text.

# Terms:
# [setose cuticle](http://purl.obolibrary.org/obo/AISM_0000530)
# [has member](http://purl.obolibrary.org/obo/RO_0002351)
# [has element count](https://github.com/sergeitarasov/PhenoScript/PHS_0000016)
# [has part](http://purl.obolibrary.org/obo/BFO_0000051)
# [cuticular seta](http://purl.obolibrary.org/obo/AISM_0000039)
# [has component](http://purl.obolibrary.org/obo/RO_0002180)
# [phs_original_assertion](https://github.com/sergeitarasov/PhenoScript/PHS_0000005)
# [phs_original_class](https://github.com/sergeitarasov/PhenoScript/PHS_0000002)
# [phs_NL](https://github.com/sergeitarasov/PhenoScript/PHS_0000004)

# inser phs_NL if it does not exist
INSERT {
  <https://github.com/sergeitarasov/PhenoScript/PHS_0000004> a owl:AnnotationProperty ;
                  rdfs:label "phs_NL" .
}
WHERE {
  FILTER NOT EXISTS {
    <https://github.com/sergeitarasov/PhenoScript/PHS_0000004> a owl:AnnotationProperty .
  }
};


# Make NL text
INSERT {
  ?col <https://github.com/sergeitarasov/PhenoScript/PHS_0000004> ?textNL .
}
WHERE {
  # Find individuals of the target class
  ?col rdf:type owl:NamedIndividual .
  ?col rdf:type [
    rdf:type owl:Restriction ;
    owl:onProperty obo:RO_0002180 ; # has_component
    owl:qualifiedCardinality ?convertedCount ; # count
    owl:onClass ?compClass ; # the class of comp (component)
  ] .
  ?compClass rdfs:label ?compClassLabel .
  # Merge NL text into one string
  BIND(CONCAT(
    "has ", STR(?convertedCount), " [", ?compClassLabel, "](",
    STR(?compClass), ");"
  )  AS ?textNL)
}