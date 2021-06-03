import os,json,math
import ttext as tk
from bs4 import BeautifulSoup
import collections
from collections import Counter
from contextlib import ExitStack
import fileinput

def visible_text(tag):
    """Function that takes a tag and returns if it is a valid tag
        @param tag: the BeautifulSoup Tag to take in
        @return: True if valid, False if invalid
    """
    # Add any more valid tags to this list of tags
    x = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'p', 'pre', 'ul', 'ol', 'b', 'a', 'cite', 'em', 'i', 'strong', 'small', 'td','th', 'tr', 'caption']
        # tag.name gets the name of the tag, otherwise you have a full html tag (ie. <a href="#">thing</a> instead of 'a')
    if tag.name in x:
        return True
    return False

def computeTF(tokens,id):
    global index
    print("\tComputing TF & Adding to Index...")
    c = Counter(tokens)

    for x in c:

        if x in index:
            posting = []
            posting.append(id)
            posting.append(c[x])
            posting.append(0)
            index[x].append(posting)
        else:
            posting = []
            posting.append(id)
            posting.append(c[x])
            posting.append(0)
            nestedPosting = []
            nestedPosting.append(posting)
            index[x] = nestedPosting

DEV =  os.path.abspath("../../lopes/Datasets/IR/DEV")
directory = os.fsencode(DEV)
f = open("doc.txt",'w')
index = {}

id = 0
offload_c = 0
offload_p = 0
partials = []
for folder in os.listdir(directory):
    folder = os.fsdecode(folder)
    DEVSUB = os.path.abspath("../../lopes/Datasets/IR/DEV/"+folder)
    directory = os.fsencode(DEVSUB)
    for file in os.listdir(directory):
        id += 1
        file = os.fsdecode(file)
        fPath = str(DEVSUB) + "/" + file
        with open(fPath,'r') as f:
            response = json.load(f)

        with open("doc.txt",'a') as f:
            f.write(str(id) + " " + response['url'] + "\n")

        # Parse HTML Doc here with beautifulsoup
        if response['encoding'] == 'ascii' or response['encoding'] == 'utf-8':
            print("\nWorking on:" + str(response['url']))
            soup = BeautifulSoup(response['content'], 'html.parser')
            text = " ".join([x.get_text().rstrip() for x in soup.find_all(visible_text)])
            subIndex = computeTF(tk.tokenizeText(text),id)
        
        offload_c += 1

        # offload
        if offload_c >= 15000:
            print("Reached {} files\n".format(offload_c))
            print("Writing partial index to file...\n")
            name = 'index{}.txt'.format(str(offload_p))

            o_index = collections.OrderedDict(sorted(index.items()))
            with open(name,'w') as f:
                for k,v in o_index.items():
                    f.write(str(k) + ": " + str(v) + "\n")
            
            index = {}
            offload_p += 1
            offload_c = 0
            partials.append(name)

if len(index) > 0:
    print("Reached {} files\n".format(offload_c))
    print("Writing partial index to file...\n")
    name = 'index{}.txt'.format(str(offload_p))
    
    o_index = collections.OrderedDict(sorted(index.items()))
    with open(name,'w') as f:
            for k,v in o_index.items():
                f.write(str(k) + ": " + str(v) + "\n")
    
    index = {}
    offload_p += 1
    offload_c = 0
    partials.append(name)

# Merge partial index files
with ExitStack() as stack:
    # list of all the files
    files = [stack.enter_context(open(fname)) for fname in partials]
    
    for f in files:
        # for each line in the current file we're reading
        for line in f:
            found = 0 # flag to know if we found the index
            
            # we check through the lines in the output
            try:
                with open("merged_index.txt", 'r') as output:
                    for mline in output:
                        if line.split(':')[0] == mline.split(':')[0]:
                            found = 1
                            break
            except:
                found == 0

            if found != 0:
                # this means that the term in f is already in the merged list
                for nline in fileinput.input(files="merged_index.txt", inplace=1):
                    if nline.split(':')[0] == line.split(':')[0]:
                        curr = eval(nline.split(':')[1])
                        curr += eval(line.split(':')[1])
                        print("{}: {}".format(nline.split(':')[0], curr))
            if found == 0:
                # the term in f is not in the merged list
                with open("merged_index.txt", 'a') as op:
                    op.write(line)

#Calculate TF-IDF
print("Calculating TF-IDF...\n")
for nline in fileinput.input(files="merged_index.txt", inplace=1):
    tokenDocs = len(eval(nline.split(':')[1]))
    tokenlist = eval(nline.split(':')[1])
    for i, posting in enumerate(eval(nline.split(':')[1]), 0):
        totalDocs = id #Total number of docs
        idf = math.log(totalDocs/tokenDocs)
        tfidf = round( (1+math.log(posting[1]))*idf,3)
        tokenlist[i][2] = tfidf
    print("{}: {}".format(nline.split(':')[0], tokenlist))