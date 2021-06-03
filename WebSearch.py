import ast, math
import ttext as tk
from collections import Counter



seeks = {}
inF = open('index.txt')
jumps = open('jumps.txt')
for x in jumps.read().split('\n'):
    if x != '':
        seeks[x.split(':')[0]] = int(x.split(':')[1])
jumps.close()
docF = open('doc.txt')
Dseeks = {}
line = docF.readline()
offset = 0
while(line != ''):
    Dseeks[int(line.split(' ')[0])] = offset
    offset += len(line)
    line = docF.readline()

def cosineSim(q):
    tokens = tk.tokenizeText(q)
    c = Counter(tokens)
    scores = {}
    length = {}
    for term in c:
        print("Processing term: " + term)
        #Get postings list for term here
        if term in seeks.keys():
            inF.seek(0)
            inF.seek(seeks[term])
            why = inF.readline()
            index[term] = ast.literal_eval(why[len(term + ': '):])
        #Calc W_t,q
        Wtq = (1+math.log(c[term])) * (index[term][0][2]/(1+math.log(index[term][0][1])))
        for posting in index[term]:
            if posting[0] in scores:
                scores[posting[0]] += posting[2] * Wtq
            else:
                scores[posting[0]] = posting[2] * Wtq
            
            if posting[0] not in length.keys():
                docLen = 0
                if posting[0] in Dseeks.keys():
                    docF.seek(0)
                    docF.seek(Dseeks[posting[0]])
                    line = docF.readline()
                    docLen = float(line.split(' ')[1])
                length[posting[0]] = docLen #Get the length value from doc.txt
        index.clear()
    for id in scores.keys():
        if length[id] > 0:
            scores[id] /= length[id]
            '''
            print("ID (" + str(id) + "): " + str(scores[id]))
            '''
    #Gets the top 5 search results
    BestHits = sorted(scores.items(), key=lambda kv: kv[1], reverse = True)[:5]
    for i in BestHits:
        docF.seek(0)
        docF.seek(Dseeks[i[0]])
        line = docF.readline()
        print(line.split(' ')[2].strip('\n'))
    

index = {}
query = input("Search: ")
cosineSim(query)
    #Sort the scores here and return top 5

inF.close()
docF.close()
