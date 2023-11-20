from owlready2 import *

# def make_phsOnto(onto):
with onto:
    class phenoscript_annotations(AnnotationProperty): pass
    class phs_implies_absence_of(phenoscript_annotations): pass
    class phs_NL(phenoscript_annotations): pass
    class phs_original_assertion(phenoscript_annotations): pass
    class phs_original_class(phenoscript_annotations): pass
    class phs_DATA_block(Thing): pass
    class phs_TRAITS_block(Thing): pass
    class phs_OTU_block(Thing): pass

phenoscript_annotations.iri     = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000001'
phs_implies_absence_of.iri      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000003'
phs_NL.iri                      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000004'
phs_original_assertion.iri      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000005'
phs_original_class.iri          = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000002'
phs_DATA_block.iri              = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000020'
phs_TRAITS_block.iri            = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000021'
phs_OTU_block.iri               = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000022'

phenoscript_annotations.label    = 'phenoscript_annotations'
phs_implies_absence_of.label     = 'phs_implies_absence_of'
phs_NL.label                     = 'phs_NL'
phs_original_assertion.label     = 'phs_original_assertion'
phs_original_class.label         = 'phs_original_class'
phs_DATA_block.label             = 'DATA Block'
phs_TRAITS_block.label           = 'TRAITS Block'
phs_OTU_block.label              = 'OTU Block'

# Connecting OTUs and traits
with onto:
    class has_trait(AnnotationProperty): pass
    class contributor(AnnotationProperty): pass
    class created_by(AnnotationProperty): pass
    class project_id(AnnotationProperty): pass
    class purl_requires(AnnotationProperty): pass
    class purl_source(AnnotationProperty): pass
    class creation_date(AnnotationProperty): pass
    class cls_project(Thing): pass
    class title(AnnotationProperty): pass

has_trait.iri       = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000017'
has_trait.label     = 'has_trait'
contributor.iri     = 'http://purl.org/dc/elements/1.1/contributor'
contributor.label   = 'contributor'
created_by.iri      = 'http://www.geneontology.org/formats/oboInOwl#created_by'
created_by.label    = 'created_by'
project_id.iri      = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000018'
project_id.label    = 'project_id'
purl_requires.iri   = 'http://purl.org/dc/terms/requires'
purl_requires.label = 'requires'
purl_source.iri     = 'http://purl.org/dc/elements/1.1/source'
purl_source.label   = 'source'
cls_project.iri     = 'https://github.com/sergeitarasov/PhenoScript/PHS_0000019'
cls_project.label   = 'project'
creation_date.iri   = 'http://www.geneontology.org/formats/oboInOwl#creation_date'
creation_date.label = 'creation_date'
title.iri           = 'http://purl.org/dc/elements/1.1/title'
title.label         = 'title'
#  return(onto)