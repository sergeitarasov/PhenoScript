# -----------------------------------------
# Settings for using owlready and Phenoscript
# -----------------------------------------
from owlready2 import *

# -----------------------------------------
# Arguments
# -----------------------------------------
phsVersion = "1.0.0"

# -----------------------------------------
# owlready
# -----------------------------------------
phs = '{https://github.com/sergeitarasov/PhenoScript}'
ns = {'phs': 'https://github.com/sergeitarasov/PhenoScript'}

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)
# set_log_level(9)