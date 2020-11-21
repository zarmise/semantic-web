# semantic-web
# Plato_Homer_Personality
This project has 4 parts:

In the first part the the data has been changed to jason and prepared to be able to use in the next parts. 

In the second part the text inside the database in separated acording to actors in the text. In is stored in a dictionary
AcText where each key belongs to an actor and the value of each key is composed of a list including dictionaries. Each of these 
dictionaries has three keys: 'Loc' which includes the location of the text, 'texte' which includes the text itself and 'Textwsd' which includes the 
disambiguated words. To increase the speed of code each passage has been tokenized. 

In the third step the ontology file is uploaded using fuseki and by means of local host we can access that and make queries.
for different words first the semantics query has been made and then the ones with maximum similarities are selected and then pleasantness,attention, sensitivity and aptitute 
are asked from the data base and stored for the actor.

In the fourth step, the ontology alignment has been fulfilled. First one distionary including, synset, concept, sensitivity, aptitude, attention, and pleasantness is accociated to each word according to the output of step 3 and all dictionaries are
collected in one list. Then based on the digit after % in synset of each word the word character is determined.
Afterwards, based on the word character and word itself the query from the databased is generated where the reference is from ubycat.owl. Finally, based on the results from query, three graphs including general graph, graph related to SameAs and genral graph including same as is updated.

  
