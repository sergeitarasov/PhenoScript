
import pandas as pd
import xml.etree.ElementTree as ET


class labels2IRI:
    def __init__(self, file):
        self.untranslated=[]
        self.countNA=0
        self.countLBS=0
        dt = pd.read_csv (file)
        key = pd.DataFrame(dt, columns= ['IRI','label.final'])
        ll=key.to_dict('records')
        self.dd={}
        for i in ll:
          #print(i)
          #dd[i['IRI']]=i['label.nospace']
          self.dd[i['label.final']]=i['IRI']
    
    def resetCount(self):
        self.countNA=0
        self.countLBS=0
    
    def translate(self, label):
        if label in self.dd:
          self.countLBS+=1
          out=self.dd[label]
          return out
        else:
          self.countNA+=1
          #print(label)
          self.untranslated.append(label)
          return 'NA'
    
    def print_untrans(self):
        self.untr=list(set(self.untranslated))
        self.untr.sort()
        print('\t Untranslated terms:')
        for item in self.untr:
            print('\t', item)
            #print(*self.unnn.sort(), sep='\n')
    
    def reset_untrans(self):
        self.untranslated=[]



# aa=['c','a','f']
# bb=list(set(aa))
# bb.sort()
# print(*bb, sep='\n')


def translatePhs(root, iriDic):
  iriDic.resetCount()
  # nodes
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node'):
    #i.set('Status', 'Completed')
    #print(nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name'))
    label=nn.get('{https://github.com/sergeitarasov/PhenoScript}node_name')
    iri=iriDic.translate(label)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
  
  print('- translated nodes: %s; NA nodes: %s.' % (iriDic.countLBS, iriDic.countNA))
  iriDic.resetCount()
  
  # print untranslated terms
  iriDic.print_untrans()
  iriDic.reset_untrans()

  # edges
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}edge'):
    #print(nn.text)
    label=nn.text
    iri=iriDic.translate(label)
    #print(iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
  print('- translated edges: %s; NA edges: %s.' % (iriDic.countLBS, iriDic.countNA))
  iriDic.resetCount()
  
  # print untranslated terms
  iriDic.print_untrans()
  iriDic.reset_untrans()
  
  # phs:node_property
  for nn in root.iter('{https://github.com/sergeitarasov/PhenoScript}node_property'):
    #print(nn.text)
    #label=nn.text
    label=nn.get('{https://github.com/sergeitarasov/PhenoScript}value')
    iri=iriDic.translate(label)
    #print(iri)
    nn.set('{https://github.com/sergeitarasov/PhenoScript}iri', iri)
  print('- translated phs:node_property: %s; NA phs:node_property: %s.' % (iriDic.countLBS, iriDic.countNA))
  iriDic.resetCount()




