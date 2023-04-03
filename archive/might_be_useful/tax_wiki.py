import pandas as pd

# Read the TSV file
taxonomy = pd.read_csv("/Users/taravser/Downloads/backbone/Taxon.tsv", sep='\t')

genus_name = "11693236"
genus_data = taxonomy[taxonomy['taxonID'] == genus_name]


#----------

# Define the chunk size (e.g., 10,000 rows)
chunksize = 100000

# Initialize an empty DataFrame to store the processed data
processed_data = pd.DataFrame()

# Read the TSV file in chunks
for chunk in pd.read_csv("/Users/taravser/Downloads/backbone/Taxon.tsv", sep='\t', chunksize=chunksize):
    # Process the chunk (e.g., filter rows or extract columns)
    # processed_chunk = process_chunk(chunk)  # Replace 'process_chunk' with your processing function
    processed_chunk = chunk[chunk['taxonID'] == 11693236]

    # Append the processed chunk to the processed_data DataFrame
    processed_data = processed_data.append(processed_chunk, ignore_index=True)

col_names = processed_data.columns
print(col_names)

Index(['taxonID', 'datasetID', 'parentNameUsageID', 'acceptedNameUsageID',
       'originalNameUsageID', 'scientificName', 'scientificNameAuthorship',
       'canonicalName', 'genericName', 'specificEpithet',
       'infraspecificEpithet', 'taxonRank', 'nameAccordingTo',
       'namePublishedIn', 'taxonomicStatus', 'nomenclaturalStatus',
       'taxonRemarks', 'kingdom', 'phylum', 'class', 'order', 'family',
       'genus'],
      dtype='object')

# -----------------

# /Users/taravser/opt/anaconda3/envs/PhenoScript/bin/pip install rdflib

import rdflib
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Create an RDF graph
g = Graph()

# Define a namespace for your taxonomy data
TAXON = Namespace("http://example.org/taxon/")
TAXON2 = Namespace("http://example2222.org/taxon/")
g.bind("taxon", TAXON)

chunksize = 10000

# Convert each row in the DataFrame to RDF triples
# remove nrow to read all
for chunk in pd.read_csv("/Users/taravser/Downloads/backbone/Insecta.tsv", sep='\t', chunksize=chunksize, nrows=10): # nrows=10
     print(chunk)
    for index, row in chunk.iterrows():
        # print(row)
        taxon_id = URIRef(TAXON[str(row['taxonID'])])
        g.add((taxon_id, RDF.type, TAXON.Taxon))
        # g.add((taxon_id, RDF.type, TAXON2.Taxon))
        g.add((taxon_id, RDF.type, rdflib.term.URIRef(':example333.org/taxon/Taxon3')))
        g.add((taxon_id, RDFS.label, Literal(row['scientificName'], datatype=XSD.string)))
        # Add more properties as needed


# Serialize the RDF graph to a file
with open('/Users/taravser/Downloads/backbone/output.ttl', 'w') as ttl_file:
    ttl_file.write(g.serialize(format='turtle'))


# --- bash, reduce file

grep '1086468' Taxon.tsv > filtered_rows.tsv
grep 'Parachorius' taxon.txt

# subsample
awk -F'\t' '$(20) == "Insecta" {print}' Taxon.tsv > Insecta.tsv # this is without header
awk -F'\t' 'NR==1 || $(20) == "Insecta" {print}' Taxon.tsv > Insecta.tsv

head -n 1 taxon.txt | awk -F '\t' '{for (i=1; i<=NF; i++) print i, $i}' # print header
# print header and next row
paste <(head -n 1 taxon.txt | tr '\t' '\n') <(head -n 2 taxon.txt | tail -n 1 | tr '\t' '\n') | column -t



# -----

import sqlite3
import pandas as pd

# Create an SQLite database in memory
conn = sqlite3.connect(':memory:')


# Read the first chunk of the TSV file
first_chunk = pd.read_csv("/Users/taravser/Downloads/backbone/Insecta.tsv", sep='\t', nrows=10)

# Print the first chunk
print(first_chunk)

# Read the TSV file in chunks and insert data into the SQLite database
chunksize = 100000

for chunk in pd.read_csv("/Users/taravser/Downloads/backbone/Insecta.tsv", sep='\t', chunksize=chunksize):
    chunk.to_sql('my_table', conn, if_exists='append', index=False)

# Create a cursor object to execute queries
cur = conn.cursor()

# Get the list of columns for a specific table
table_name = "my_table"
cur.execute(f"PRAGMA table_info({table_name})")

# Fetch the results and extract the column names
columns = [info[1] for info in cur.fetchall()]

# Print the column names
print(columns)

# Perform an SQL query on the data
query_result = pd.read_sql_query("""SELECT taxonID, parentNameUsageID, acceptedNameUsageID, scientificName, canonicalName, taxonRank, taxonomicStatus, nomenclaturalStatus
FROM my_table 
WHERE taxonID = 1086468""", conn)

query_result = pd.read_sql_query("""SELECT taxonID, parentNameUsageID, acceptedNameUsageID, scientificName, canonicalName, taxonRank, taxonomicStatus, nomenclaturalStatus, genus
FROM my_table 
WHERE acceptedNameUsageID = 1086468""", conn)
print(query_result)

query_result = pd.read_sql_query("""SELECT taxonID, parentNameUsageID, acceptedNameUsageID, originalNameUsageID, scientificName, canonicalName, taxonRank, taxonomicStatus, nomenclaturalStatus, genus
FROM my_table 
WHERE genus = 'Parachorius'""", conn)
print(query_result)


query_result = pd.read_sql_query("""
WITH RECURSIVE hierarchy(taxonID, canonicalName, parentNameUsageID) AS (
    -- Base case: Select the employee with a specific id
    SELECT taxonID, canonicalName, parentNameUsageID FROM my_table WHERE taxonID = 1086468
    UNION ALL
    -- Recursive step: Select the manager of the previous level employee
    SELECT e.taxonID, e.canonicalName, e.parentNameUsageID
    FROM my_table e
    JOIN hierarchy h ON e.taxonID = h.parentNameUsageID
)
SELECT * FROM hierarchy;
""", conn)


print(query_result)


# Close the cursor
cur.close()

# Close the connection
conn.close()

Index(['taxonID', 'datasetID', 'parentNameUsageID', 'acceptedNameUsageID',
       'originalNameUsageID', 'scientificName', 'scientificNameAuthorship',
       'canonicalName', 'genericName', 'specificEpithet',
       'infraspecificEpithet', 'taxonRank', 'nameAccordingTo',
       'namePublishedIn', 'taxonomicStatus', 'nomenclaturalStatus',
       'taxonRemarks', 'kingdom', 'phylum', 'class', 'order', 'family',
       'genus'],
      dtype='object')