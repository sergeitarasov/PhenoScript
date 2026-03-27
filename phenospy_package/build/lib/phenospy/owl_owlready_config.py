# -----------------------------------------
# Settings for using owlready and Phenoscript
# -----------------------------------------
from owlready2 import *
import pkg_resources
# -----------------------------------------
# Arguments
# -----------------------------------------

phsVersion = pkg_resources.get_distribution("phenospy").version

# -----------------------------------------
# owlready
# -----------------------------------------
phs = '{https://github.com/sergeitarasov/PhenoScript}'
ns = {'phs': 'https://github.com/sergeitarasov/PhenoScript'}

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
# set_log_level(9)