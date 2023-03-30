from pygbif import species
import json
import csv
import pandas as pd


# -----------------------------------------
# Queries genera and their species from Gbif and returns csv output for Robot
# -----------------------------------------

# genera = ['Xinidium', 'Macroderes']
# dt=get_fromGbifGenera(genera)
# dt
# header = {'ID': 'ID', 'Label': 'A rdfs:label', 'Type': 'TYPE'}
# header = pd.DataFrame(header, index=[0])
# result = pd.concat([header, dt], ignore_index=True)
# result
# result.to_csv('/Users/taravser/Documents/My_papers/taxonomy-repo/csv/gbifTaxa.csv', index=False)


# get_fromGbifGenus('Xinidium')
def get_fromGbifGenus(genus):
    # Parent
    parent = species.name_backbone(name= genus, rank='genus', order = 'Insecta')
    # pretty_result = json.dumps(parent, indent=4, sort_keys=True)
    # print(pretty_result)

    # Parent get info
    parent_name_usage = species.name_usage(key=parent.get('usageKey'), data='all')
    # pretty_result = json.dumps(parent_name_usage, indent=4, sort_keys=True)
    # print(pretty_result)


    # Kids Query 
    kids_name_usage = species.name_usage(key=parent_name_usage.get('key'), data='children', limit=2000)
    # pretty_result = json.dumps(kids_name_usage, indent=4, sort_keys=True)
    # print(pretty_result)

    # Extract the 'results' field containing the children taxa
    children = kids_name_usage['results']
    children.append(parent_name_usage)

    # Create a list to store the extracted data
    data = []

    # Extract the 'species' and 'taxonID' fields for all children
    for child in children:
        if child.get('canonicalName') is not None:
            IRI = 'https://www.gbif.org/species/' + str(child.get('key'))
            label = child.get('canonicalName')
            obj_type ='class'
            # data.append({
            #     'ID': IRI, 
            #     'A rdfs:label': label,
            #     'TYPE': obj_type
            #     })
            data.append({
                'ID': IRI, 
                'Label': label,
                'Type': obj_type
                })


    # Save the extracted data as a CSV file
    data_frame = pd.DataFrame(data)
    return data_frame


def get_fromGbifGenera(genera):
    data = pd.DataFrame()
    for genus in genera:
       # data.concat(get_fromGbifGenus(genus))
       data = pd.concat([data, get_fromGbifGenus(genus)], ignore_index=True)
    return data




