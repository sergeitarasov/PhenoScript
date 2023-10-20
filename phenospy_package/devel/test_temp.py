# /Users/taravser/anaconda3/envs/PhenoScript/bin/python

from owlready2 import *
import os

set_log_level(9)

onto_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package/phenospy/package-data/phenoscript.owl'
owl_file = '/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/PhenoScript/phenospy_package/devel/test_temp.owl'

onto = get_ontology(onto_file).load()

def render_using_label(entity):
    return entity.label.first() or entity.name

set_render_func(render_using_label)



# with tempfile.NamedTemporaryFile() as f:
#     onto.save(file=f.name, format="rdfxml")
#     # print("Ontology saved to:", f.name)
#     f.close()
#     onto.destroy()
#     onto = get_ontology(f.name).load()


temp = tempfile.NamedTemporaryFile(suffix=".owl", delete=False)
onto.save(file=temp.name, format="rdfxml")
temp.close()
onto.destroy()
onto = get_ontology(temp.name).load()
os.unlink(temp.name)


temp.name

onto.save(file = owl_file, format = "rdfxml")


#---------------
from owlready2 import *
set_log_level(9)

onto = get_ontology("http://test.org/onto.owl")

with onto:
    class Drug(Thing):
        pass

my_drug = Drug("my_drug")
ins2 = Drug("urn:uuid938")
ins2.iri = "aaa//urn:uuid938111"
print(ins2.iri)

onto.save(file = 'test_temp.owl', format = "rdfxml")

#---

import datetime


def current_datetime_xsd():
    # Get the current date and time with microseconds
    current_time = datetime.datetime.now()
    # Remove microseconds from the time
    current_time_without_microseconds = current_time.replace(microsecond=0)
    # Format it as xsd:dateTime
    # xsd_datetime = current_time_without_microseconds.isoformat()
    return current_time_without_microseconds

# Example usage
xsd_date_time = current_datetime_xsd()
print(xsd_date_time)

datetime.date
datetime.datetime(xsd_date_time)
ins2.comment = 'asas'
dd=datetime.date(2022, 1, 15)
dd.isoformat()
dd=datetime.datetime(2022, 1, 15, 18, 55)
print(dd.isoformat())


datetime.datetime()
ins2.comment=['3333', 4, dd, datetime.datetime.now()]
ins2.comment=datetime.datetime.now()
onto.save(file = 'test_temp.owl', format = "rdfxml")

# -----

class Hex(object):
    def __init__(self, value):
        self.value = value

def parser(s):
    return Hex(int(s, 16))

def unparser(x):
    h = hex(x.value)[2:]
    if len(h) % 2 != 0: return "0%s" % h
    return h

declare_datatype(Hex, "http://www.w3.org/2001/XMLSchema#hexBinary", parser, unparser)

x=Hex(int('11', 10))
hex(x.value)

parser(14)

ins2.comment=[Hex(14), dd, datetime.datetime.now()]
onto.save(file = 'test_temp.owl', format = "rdfxml")


with onto:
    class new_dp(DataProperty): pass

ins2.new_dp.append('nnnnn')
ins2.new_dp.append(3)
ins2.new_dp.append(Hex(14))


class anyURI(object):
    def __init__(self, value):
        self.value = value

def anyURI_parser(s):
    return anyURI(s)

def anyURI_unparser(x):
    return x.value

declare_datatype(anyURI, "http://www.w3.org/2001/XMLSchema#anyURI", anyURI_parser, anyURI_unparser)

ins2.comment=[anyURI('https://www.gbif.org/species/10360397')]
ins2.new_dp.append(anyURI('https://www.gbif.org/species/10360397'))
onto.save(file = 'test_temp.owl', format = "rdfxml")



from urllib.parse import urlparse
parsed_uri = urlparse('https://www.gbif.org/species/10360397')
parsed_uri = urlparse(1)
all([parsed_uri.scheme, parsed_uri.netloc])
is_valid_uri('https://www.gbif.org/species/10360397')
is_valid_uri('1')

def is_valid_uri(uri_string):
    try:
        parsed_uri = urlparse(uri_string)
        return all([parsed_uri.scheme, parsed_uri.netloc])
    except ValueError:
        return False

#------
ins2.new_dp=[]
onto.save(file = 'test_temp.owl', format = "rdfxml")
N1 = ins2
Ed = new_dp
N2 = 'https://www.gbif.org/species/10360397'
if 'http://www.w3.org/2000/01/rdf-schema#label' in Ed.iri:
    exec('N1.%s = N2' % Ed.name)
    #phs_original_assertion[N1, Ed, N2] = True
    print('opt 1')
elif (is_valid_uri(N2)):
    # ins2.new_dp.append(anyURI('https://www.gbif.org/species/10360397'))
    exec('N1.%s.append(anyURI(N2))' % Ed.name)
    #phs_original_assertion[N1, Ed, N2] = True
    comment[N1, Ed, anyURI(N2)] = True
    print('is_val')
else:
    exec('N1.%s.append(N2)' % Ed.name)
    #phs_original_assertion[N1, Ed, N2] = True
    print('opt 3')


N2
xx=anyURI(N2)
xx + 'asas'
str(xx)
type(xx)
isinstance(xx, str)

type(N1.new_dp[0])

#-----
onto.metadata.label.append('some lab')
label[onto.metadata, label, 'some lab']='annot lab'


ins2.label.append('ins lab')
label[ins2, label, 'ins lab'] = 'annot lab2'



import yaml

# Load YAML data from a file
with open('/Users/taravser/Library/CloudStorage/OneDrive-UniversityofHelsinki/My_papers/PhenoScript_main/Phenoscript-Descriptions/phenoscript_grebennikovius/sergei-tests/for_Jim/phs-config.yaml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Access and work with the YAML data
yaml_data["project-title"]
print(yaml_data)
for ontology in yaml_data["project-title"]:
    print()


ss='Description of Grebennikovius species'
ss[:35] + '...'