import json
from SPARQLWrapper import SPARQLWrapper
from nltk.corpus import wordnet as wn
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, XSD
import requests

with open('C:/Users/zarmi/Desktop/WS Project/step_3/step_3.json', 'r') as input_file:
    main4 = json.load(input_file)


texts_words = main4.get('ONTOSENTICNET_RESULTS')
#Collect all words data in one list
allwords=list()
for words in texts_words.values():
    for word in words:
        allwords+=[{
         "synset": wn.synset(word["word"]).lemmas()[0].key(),
         "concept": word["concept"],
         "sensitivity": word["sensitivity"],
         "aptitude": word["aptitude"],
         "attention": word["attention"],
         "pleasantness": word["pleasantness"],
          }]

counter=0
#initialize Graphs for ontology alignment  
GRAPH_General = Graph()
GRAPH_SameAs = Graph()
GRAPH_General_plus_SameAs= Graph()

for tmp in allwords:# For each word (tmp) in allwords list  
    if counter < 1000000: # To control the number of queries while debugging
        counter=counter+1   
        print('counter')
        print(counter)
        wordcomplete=tmp["synset"]
        word=wordcomplete.split("%")[0]

        # To find out what is the the word character
        if wordcomplete.split("%")[1][0]== "1":
           pos='noun'
        elif wordcomplete.split("%")[1][0]== "2":
           pos='verb'    
        elif wordcomplete.split("%")[1][0]== "3":
           pos='adjective'    
        elif wordcomplete.split("%")[1][0]== "4":
           pos='adverb'    
        else: 
           pos='adjective'
           
        try:
            # Make query based on word character and and word itself
            Q='SELECT ?ref ?obj WHERE {?ref <http://purl.org/olia/ubyCat.owl#externalReference> ?object filter(contains(str(?object), "[POS: %s] %s"))}' % (pos, wordcomplete)
            response = requests.post('http://localhost:3030/WN3/sparql',
              data={'query': Q}) 

            tmp1=response.json()
            reference = tmp1.get("results").get("bindings")[0].get("ref")
            out=reference.get("value").split("#")[0]
            print("Query was ok and the output is")
            print(out)
        except:
           print("There is a problem in the query")
        lemon = URIRef(out)
        urn = Namespace("urn:absolute:ontosenticnet#")
        owl = Namespace("http://www.w3.org/2002/07/owl#")
        # adding triples to the graph
        GRAPH_General.add((lemon, urn.text, Literal(
        tmp["concept"])))
        GRAPH_General.add((lemon, urn.pleasantness, Literal(
        tmp["pleasantness"], datatype=XSD.decimal)))
        GRAPH_General.add((lemon, urn.attention, Literal(
        tmp["attention"], datatype=XSD.decimal)))
        GRAPH_General.add((lemon, urn.sensitivity, Literal(
        tmp["sensitivity"], datatype=XSD.decimal)))
        GRAPH_General.add((lemon, urn.aptitude, Literal(
        tmp["aptitude"], datatype=XSD.decimal)))
        
        
        concept = URIRef("https://sentic.net/api/en/concept/%s" % ("_".join(
        tmp["concept"].split(" "))))
        GRAPH_SameAs.add((lemon, owl.sameAs, concept))
        
    
        GRAPH_General_plus_SameAs.add((lemon, owl.sameAs, concept))
        GRAPH_General_plus_SameAs.add((concept, urn.pleasantness, Literal(
            tmp["pleasantness"], datatype=XSD.decimal)))
        GRAPH_General_plus_SameAs.add((concept, urn.attention, Literal(
            tmp["attention"], datatype=XSD.decimal)))
        GRAPH_General_plus_SameAs.add((concept, urn.sensitivity, Literal(
            tmp["sensitivity"], datatype=XSD.decimal)))
        GRAPH_General_plus_SameAs.add((concept, urn.aptitude, Literal(
            tmp["aptitude"], datatype=XSD.decimal)))
        
        
#Serializing the graph and storing        
GRAPH_General.serialize(destination="aligned_ontologies_General_modif.nt", format="nt")
GRAPH_SameAs.serialize(destination="aligned_ontologies_SameAs_modif.nt", format="nt")
GRAPH_General_plus_SameAs.serialize(destination="aligned_ontologies_General_plus_SameAs_plus_SameAs_modif.nt", format="nt")

  