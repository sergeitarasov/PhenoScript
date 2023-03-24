from urllib.parse import urlsplit

iris = [
    "https://example.org/ontology1/class1",
    "https://example.org/ontology2/class2",
    "https://example.org/ontology1/class3",
]

iris = [
    "http://purl.obolibrary.org/obo/PATO_000111",
    "http://purl.obolibrary.org/obo/PATO_000112",
    "http://purl.obolibrary.org/obo/PATO_000113",
    "http://purl.obolibrary.org/obo/HAO_000111",
    "http://purl.obolibrary.org/obo/pato#increased",
    "http://purl.obolibrary.org/obo/pato#deincreased",
    "http://purl.obolibrary.org/obo/has_some",
     "http://purl.obolibrary.org/obo/has_some2"
]

namespaces = set()

for iri in iris:
    split_iri = urlsplit(iri)
    namespace = f"{split_iri.scheme}://{split_iri.netloc}{split_iri.path.rsplit('/', 1)[0]}"
    namespaces.add(namespace)

print(namespaces)

#------

from urllib.parse import urlparse
from os.path import commonprefix

def find_common_namespace(iris):
    # Parse the IRIs and extract the path component
    paths = [urlparse(iri).path for iri in iris]
    
    # Find the longest common prefix
    common_path = commonprefix(paths)
    
    # If the common prefix ends with a '/', return it as the namespace
    if common_path.endswith('/'):
        return common_path
    else:
        # Otherwise, find the last '/' in the common prefix and return the substring up to it
        last_slash_index = common_path.rfind('/')
        return common_path[:last_slash_index + 1]

# Example usage
iris = [
    'http://purl.obolibrary.org/obo/HAO_0000123',
    'http://purl.obolibrary.org/obo/HAO_0000456',
    'http://purl.obolibrary.org/obo/HAO_0000789',
]

namespace = find_common_namespace(iris)
print(namespace)
