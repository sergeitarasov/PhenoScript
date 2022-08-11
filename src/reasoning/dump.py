

ind=[]
for i in onto.individuals():
    ind.append(i)
    print(i)

for i in onto.classes():
    print(i)




onto.search(label = "apical")
# BFO_0000051 has part
# BFO_0000050 part of
ind[0].inverse_restrictions(obo.BFO_0000051)
ind[0].get_properties()
ind[0].INDIRECT_get_properties()
ind[0].INDIRECT_label

ind[0].BFO_0000051
ind[0].is_a
ind[0].INDIRECT_is_a
ind[1].INDIRECT_is_a.
ind[1].descendants()
print(*ind[1].INDIRECT_is_a, sep='\n')

# region of cuticle
obo.AISM_0000174
list(obo.AISM_0000174.subclasses())
list(obo.AISM_0000174.descendants())
list(obo.AISM_00E00174.ancestors())

list(onto.classes())

ind[1].BFO_0000050.append(ind[2])
ind[0].is_a

for prop in ind[1].get_properties():
    for value in prop[ind[1]]:
        print(".%s == %s" % (prop.python_name, value), prop.is_a)

obo.BFO_0000050[ind[0]]
obo.BFO_0000050[ind[3]]
obo.BFO_0000050
Inverse(obo.BFO_0000050)

# find ancestors
ins=ind[0]
ins.INDIRECT_BFO_0000050
ins.INDIRECT_BFO_0000051
ins.is_a
ins.BFO_0000050
isinstance(ins, Thing)

ins.BFO_0000050
ins.inverse_restrictions(obo.BFO_0000051)

# find superparts of an instance
ins=ind[2]
def superParts(ins):
    results = []
    ance=ins.BFO_0000050.first()
    if (ance is not None and isinstance(ance, Thing)):
        results.append(ance)
        #print('results', results)
        results.extend(superParts(ance))
    #return results
    return list(set(results))

superParts(ind[2])


# turn down inverse props
obo.BFO_0000050
obo.BFO_0000050.inverse=[]
ind[1].BFO_0000050.append(ind[2])
obo.BFO_0000050.inverse=obo.BFO_0000051
#---------------------

## a/p reasonin for region of cuticle
topClass=obo.AISM_0000174
list(topClass.descendants(include_self = False))
list(topClass.subclasses())

obo.AISM_0000174.is_a
obo.AISM_0000174.get_class_properties()
issubclass(obo.AISM_0000174, Thing)
issubclass(obo.BFO_0000050, Thing)

for i in topClass.descendants(include_self = False):
    #print(i)
    #print(issubclass(i, Thing))
    if issubclass(i, Thing)==False:
        print(i)