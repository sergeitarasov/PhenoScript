----
tree
for child in root1:
  print(child.tag, child.attrib)

root1.findall(".")
grades =root1.findall('.//{https://github.com/sergeitarasov/PhenoScript}node')
grades[1].attrib
grades[1].tag
grades[1].get('{https://github.com/sergeitarasov/PhenoScript}node_id')
unique_grades = list(set(g.text for g in grades))

#tags = {elem.tag for elem in tree.iter()}

#---
  # get all nodes
  #xml_ns_strip(PS)
  allN <- xml_find_all(PS, ".//phs:node")
  un.id <- xml_attr(allN, attr='node_id') %>% unique()

  #-- for speeding up
  allN.node_id=xml_attr(allN, attr='node_id')
  #length(allN.node_id)
  date <-  Sys.Date()
  date <-str_replace_all(date, '-','.')
  #--

# aa=['c','a','f']
# bb=list(set(aa))
# bb.sort()
# print(*bb, sep='\n')
#-----------------
allN=root1.findall('.//phs:node', ns_xml)
len(allN)

#xml_find_all(PS, './/phs:nested_node[@phs:triple_pos="1"] | //phs:list_node[@phs:triple_pos="1"]')

allN=root1.findall('.//phs:node[@phs:fromNegativeEdge="False"]', ns_xml)
len(allN)

allN[1].get('{https://github.com/sergeitarasov/PhenoScript}node_id')
allN[1].get('{https://github.com/sergeitarasov/PhenoScript}node_id')
allN[1].attrib

allN_node_id=[]
for n in allN:
  allN_node_id.append(n.get(str_ns_xml+'node_id'))
  print(n.get(str_ns_xml+'node_id'))


len(allN_node_id)
un_id=list(set(allN_node_id))
len(un_id)

i=un_id[0]
root1.findall(".//{https://github.com/sergeitarasov/PhenoScript}node[@{https://github.com/sergeitarasov/PhenoScript}node_id='%s']"%i)

#-----------
ns_xml = {'phs': 'https://github.com/sergeitarasov/PhenoScript'}
str_ns_xml='{https://github.com/sergeitarasov/PhenoScript}'

for neighbor in root1.iter('{https://github.com/sergeitarasov/PhenoScript}fromNegativeEdge'):
  #print(neighbor.attrib)
  print(neighbor)



