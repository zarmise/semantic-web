import json
from nltk.corpus import wordnet as wn
import requests
with open('C:/Users/zarmi/Desktop/WS Project/step_2/plat.tet45_wsd.json', 'r') as jfile:
     main3 = json.load(jfile)
#%%

Sim_L = []
Syns_L = []
Syns_D = {}
outAct={} 
similarity_dict = dict()
counter_actor=0

for Actor in main3:
    Act=main3[Actor]
    outAct[Actor]=[]
    similarity_list = list()
    counter_actor=counter_actor+1
    print('the actor is')
    print(Actor)
    if counter_actor<18:
        counter_part=0
        for tmp1,part in enumerate(Act):
            counter_part=counter_part+1
            if counter_part<10000000: # To limit the number of instances because it takes long time to run
                for tmp2, wsd in enumerate(part['Textwsd']):
                    if wsd[2] is not None:
                        wsd[2] = wn.synset(wsd[2])# change each word to synset eg. contest.n.01 to Synset('contest.n.01')
                        completeword=wsd[2]
                        dictword = dict() #Initializing the dictionary of word data      
                        word1 = completeword.name()# change each synset to word eg.  Synset('contest.n.01') to contest.n.01 
                        pureword = word1[:-5]# get the pure word string eg 'contest.n.01' to contest                    
                        dictword["word"] = completeword # store in 'word' key the synset eg Synset('contest.n.01')
                        # prepare query from ontosenticnet
                        Q='PREFIX owl: <http://www.w3.org/2002/07/owl#>             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>             PREFIX urn: <urn:absolute:ontosenticnet#>                  SELECT *             WHERE {                 ?word urn:text "%s".                     ?word urn:semantics ?semantics             }'% (pureword)
                        try:
                            response = requests.post('http://localhost:3030/ontosenticnet1/sparql',
                              data={'query': Q})
                            query_result = response.json()
                            results = query_result.get("results").get("bindings")#getting the semantics from the ontosenticnet
                            dictword["semantics"]=[r.get('semantics').get("value").replace("urn:absolute:ontosenticnet#","") for r in results]                
                            if len(dictword.get("semantics")) > 0:
                                wordmaxtest = dictword.get("word")
                                synsem = dict()
                                similaritynumericalvalue=0                           
                                for semantic in dictword.get("semantics"):
                                    synsem[semantic] = wn.synsets(semantic)
                                sims = dict()
                               
                                for key in synsem.keys():#key is onlz the string of semantics
                                    if synsem[key]:
                                        sims[key] = list()
                                    # Ajouter la liste des similarités pour chaque synset (des concepts)
                                    
    #                                 if semantics_synsets[key] is not empty:
                                        for semant in synsem[key]:
                                            if wn.wup_similarity(wordmaxtest, semant) is not None and wn.wup_similarity(wordmaxtest, semant)>similaritynumericalvalue:
                                                similaritynumericalvalue=wn.wup_similarity(wordmaxtest, semant)
                                                similaritybestsynset=semant
                                if similaritybestsynset:
                                   similarity_list.append([similaritynumericalvalue,wordmaxtest,similaritybestsynset]) 
                    
                        except:
                            print('The query failed')   
                        
    similarity_dict[Actor] = similarity_list
similarities=similarity_dict
sims= similarities 
#%% 
text_data = dict()
for key, similarities1 in sims.items():
    # Préparation des données, récupération des infos dans OntoSenticNet
    text_data_list = list()
    for simil in similarities1:
        if (simil is not None) and (simil[0] > 0):
            wordmeta=simil[2].name().split('.')[0]
            Q='PREFIX owl: <http://www.w3.org/2002/07/owl#>                 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                 PREFIX urn: <urn:absolute:ontosenticnet#>                              SELECT *                 WHERE {                     ?word urn:text "%s".                          ?word urn:sensitivity ?sens.                               ?word urn:aptitude ?apt.                        ?word urn:attention ?att.                          ?word urn:pleasantness ?plea.                 }'% (wordmeta)
            try:
                responsemeta = requests.post('http://localhost:3030/ontosenticnet1/sparql',
                  data={'query': Q})               
                query_result = responsemeta.json()
                # print('Querz result is')
                # print(query_result )
                results = query_result.get("results").get("bindings")
                # Si on a un résultat, on nettoie l'output et retourne
                if len(results) > 0:
                    r = results[0]
                    del r["word"]
                    # Mise en forme de l'output
                    for metadata in r.keys():
                        val = r[metadata].get("value")
                        r[metadata] = val
                    outp= r
                else:
                    outp= None
                    
                if outp:
                    meta_data = outp
                    text_data_list.append({"word": simil[1].name(),"concept": simil[2].name().split('.')[0],
                        "sensitivity": meta_data["sens"],
                        "aptitude": meta_data["apt"],
                        "attention": meta_data["att"],
                        "pleasantness": meta_data["plea"],
                    })        
            except:
                print('failed')

    # Ajouter les données au dictionnaire
    text_data[key] = text_data_list
output=text_data
print('output is')
print(output)
with open('./step_3.json', 'w') as output_file:
    json.dump({"Title": 'Plato in Twelve Volumes, Vol. 8 translated by W.R.M. Lamb.',"Author": 'Plato',"ONTOSENTICNET_RESULTS": output
    }, output_file)
 