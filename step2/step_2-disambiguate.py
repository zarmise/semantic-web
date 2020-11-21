import json
from pywsd import disambiguate
from pywsd.similarity import max_similarity as maxsim
from nltk import tokenize

#%% Opening
with open('C:/Users/zarmi/Desktop/platon/etape1/plat.tet45_eng.json', 'r') as jfile:
    main = json.load(jfile)
#%%
title = main["TEI.2"]["teiHeader"]["fileDesc"]["titleStmt"]["title"]
author = main["TEI.2"]["teiHeader"]["fileDesc"]["titleStmt"]["author"]



#%% Making a list of all Actors 
Actors=[]  
for c,item in enumerate(main['TEI.2']['text']['group']['text']):
    print(c)
    print(type(item))
    item1=[]
    for c1,item1 in enumerate(item['body']['castList']['castItem']):
        # print(item1)
        if isinstance(item1,dict):
            if not item1['role'] in Actors:
               Actors.append(item1['role'])
print(Actors)
    
#%% make a dictionary for actors including Text for the dialouges and Textwsd for sensed each word  
AcText = dict()
for item in Actors:
    AcText.update({item: []})


# for  i,a in enumerate(Actors):
#       AcText[a]=[]

#%%
    # initialize the output file
outfile = dict.fromkeys(['Titre','Actors'])

outfile['Titre']= title
outfile['auteur']= author
outfile['Actors'] = list()
for item in Actors:
    outfile['Actors'].append({'Actors': item, 
                                   'TXT': AcText[item]})

#%% Extract Text of each actor
for  c,item in enumerate(main['TEI.2']['text']['group']['text']):
    item2=item['body']
    if 'sp' in item2:
        if isinstance(item2['sp'],list):
            print(c)
            for c3,item3 in enumerate(item2['sp']):
                if item3['speaker'] in AcText:
                    if isinstance(item3['p'],dict):
                        print(c3)
                        TXT=item3['p']['#text']
                        if 'milestone' in item3['p']:
                            if isinstance(item3['p']['milestone'],list):
                                LOC=item3['p']['milestone'][0]['@n']
                            else:
                                LOC=item3['p']['milestone']['@n']
                        AcText[item3['speaker']].append({'Loc':LOC,'texte':TXT,'Textwsd':[]})
                    elif isinstance(item3['p'],str):   
                        print(c3)
                        print(item3['p'])
#%%
counter=0                        
for tmp1, act in enumerate(Actors): # for each actor in act
#     act=Actors[0]
    print(act)
    for tmp2, txtuntkn in enumerate(AcText[act]): # for each actorgs untikenized text in txtuntkn;
    #         txtuntkn=AcText[act][0]
    #         print(txtuntkn['texte'])
       txttkn=tokenize.sent_tokenize(txtuntkn['texte'])
    #         print(txttkn)
    #         print(txttkn)# tokenized text
       for tmp3, sent in enumerate(txttkn): # for each sentenxe in tokenzed text of eaxh actor in sent
    #             sent=txttkn[0]
                  # wordlist=sent.split()
                 # for wrd in wordlist:
           try:
               # if counter <2:
                  dissent=disambiguate(sent, algorithm=maxsim, similarity_option='wup', keepLemmas=True)
                  counter=counter+1
                  print(counter)
                  print(dissent)
                  for tmp4, diswrd in enumerate(dissent):
                      print(diswrd)
                      if diswrd[2] is not None:
                            diswrd_brief=(diswrd[0],diswrd[1],diswrd[2].name())
                            txtuntkn['Textwsd'].append(diswrd_brief)
           except:
                   pass
        #             sent=sent.replace('\n',' ')
             
#             print(tmp3)
#             print(disambiguate(sent, algorithm=maxsim, similarity_option='wup', keepLemmas=True))
with open('C:/Users/zarmi/Desktop/platon/etape2/plat.tet45_wsd.json', 'w') as out:
    json.dump(AcText, out, indent=2)                       


    
    

   
    

