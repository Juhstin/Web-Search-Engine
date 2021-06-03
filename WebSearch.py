import ast, math
import ttext as tk
from collections import Counter


'''
index = {}
query = input("Search: ")
tokens = tk.tokenizeText(query)
numTokens = len(tokens)
def Intersect(p1, p2) -> list:
    p1.sort(key = lambda x: x[0])
    p2.sort(key = lambda x: x[0])
    answer = []
    i = len(p1)
    j = len(p2)
    p1iter = iter(p1)
    posting1 = next(p1iter)
    p2iter = iter(p2)
    posting2 = next(p2iter)
    while i != 0 and j != 0:
        if posting1[0] == posting2[0]:
            answer.append(posting1)
            i -= 1
            j -= 1
            if(i != 0 and j != 0):
                posting1 = next(p1iter)
                posting2 = next(p2iter)
        elif posting1[0] < posting2[0]:
            i -= 1
            if(i != 0):
                posting1 = next(p1iter)
        else:
            j -= 1
            if(j != 0):
                posting2 = next(p2iter)
    return answer
with open("index.txt",'r') as f:
    for x in f.read().split('\n'):
        #if query == x[:len(query)]:
        #    index[query] = ast.literal_eval(x[len(query + ': '):])
        #    break
        for token in tokens:
            if token == x.split(':')[0]:
                index[token] = ast.literal_eval(x[len(token + ': '):])
                numTokens -= 1
                break
        if numTokens == 0:
            break
nameSmallest = ""
smallest = []
for token in index.items():
    if len(smallest) == 0:
        smallest = token[1]
        nameSmallest = token[0]
    elif len(token[1]) < len(smallest):
        smallest = token[1]
        nameSmallest = token[0]
del index[nameSmallest]
answers = smallest
if len(index.values()) > 0:
    for i in index.values():
        answers = Intersect(answers,i);
#remove the next for loop when we need the tf-idf in the full merged list
response = []
for i in answers:
    response.append(int(i[0]))
#answers hold all the valid pages where the words intersect, with all three elements 
finalResult = []
with open("doc.txt", 'r') as f:
    for x in f.read().split('\n'):
        y = int(x.split(' ')[0])
        if y in response:
            finalResult.append(x.split(' ')[1])
for i in finalResult[:5]:
    print(i)
    
#print(index[query])
'''
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
