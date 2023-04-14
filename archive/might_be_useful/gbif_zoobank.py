from pygbif import species
import json
import csv
import pandas as pd

species.name_backbone(name= 'Parachorius lannathai', rank='species', order = 'Insecta')
species.name_usage(key=parent.get('usageKey'), data='all')

# --- BASH

# Parachorius bolavensis: backbone taxonomy
# https://www.gbif.org/species/9536093
curl -X GET 'https://api.gbif.org/v1/species/9536093' | jq
# this returns name usage with zoobank ids
curl -X GET 'https://api.gbif.org/v1/species/9536093/related' | jq

# Parachorius bolavensis: with zoobank id
# https://www.gbif.org/species/128694326
curl -X GET 'https://api.gbif.org/v1/species/128694326' | jq

# Parachorius bolavensis: reference
# https://www.gbif.org/species/175557431/verbatim
curl -X GET 'https://api.gbif.org/v1/species/175557431' | jq

