import sys, re
from nltk import PorterStemmer
import multiprocessing

def ps(x):
    return PorterStemmer().stem(x)

def checkdigit(x):
    """Checks if the string x is an int without going into try/catch"""
    # If we have a digit, check that the length is greater than 4 (0-9999 only)
    if x.isdigit():
        if len(x) >= 4:
            return True
        return False
    # If it isn't a digit, it's chillin
    return True

def tokenizeText(wb_text)->list:
    """ Efficiency will be O(N) here, running in linear time with respect to the complexity """
    noStem = [x for x in (sum([re.findall(r'(?:[\w]+)', wb_text.lower(), flags=re.ASCII)], [])) if checkdigit(x)]
    
    with multiprocessing.Pool() as pool:
        return pool.map(ps, noStem)
    # return [PorterStemmer().stem(x) for x in (sum([re.findall(r'(?:[\w]+)', wb_text.lower(), flags=re.ASCII)], []))]

def computeWordFrequencies(tokens)->map:
    """ Efficiency will be O(N) here, running in linear time with respect to the complexity """
    # return {x : tokens.count(x) for x in tokens}
    UniqueWords = set(tokens)
    return {x : tokens.count(x) for x in UniqueWords}


def print_freq(frequencies):
    """ Efficiency will be O(N Log N) here, running in logarithmic time with respect to the complexity """
    f = open("WordCount.txt",'w')
    f.write('"Word","Count"\n')
    for x in sorted(frequencies.items(), key=lambda x: (-x[1], x[0]), reverse=False): 
        f.write('"{}","{}"\n'.format(x[0], x[1]))
    f.close()