def turnOffInverse(prop, propInv, ontoObj):
    prop.inverse = []
    for i in ontoObj.individuals():
        for target in prop[i]:
            print(target)
            #target.BFO_0000051.append(i)
            exec('target.%s.append(i)' % propInv.name)
        for target in propInv[i]:
            print(target)
            #target.BFO_0000050.append(i)
            exec('target.%s.append(i)' % prop.name)
    #
    # turn back the inverse
    #obo.BFO_0000050.inverse = obo.BFO_0000051
    prop.inverse = propInv