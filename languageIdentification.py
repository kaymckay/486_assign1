"""Kayla McKay (kaymckay)"""
import os
import sys
import math 

def trainBigramLanguageModel(text):
    """Function to train a bigram language model. """
    unigram = {}
    diagram = {}
    total = 0
    prev = " "
    for l in text:
        if l.isupper():
            l = l.lower()
        #if l.isalpha() or l.isdigit() or l == "." or l == "'" or "(" or ")":
        # if not l == "\n":
        total += 1

        #unigram
        if l in unigram:
            unigram[l] += 1
        else:
            unigram[l] = 1
        
        #diagram
        if (prev + l) in diagram:
            diagram[prev + l] += 1
        else:
            diagram[prev + l] = 1
        prev = l

    unigram["total"] = total
    # return dictionary of character frequencies
    return unigram, diagram



def identifyLanguage(text, langs, unigrams, diagrams):
    """Function to determine the language of a string.  """
    # calculate english
    p_e = 1
    prev = ""
    V = len(unigrams[0]) - 1
    for t in text:
        p_t = 0
        # start
        t = t.lower()
        if prev == "":
            val = unigrams[0][t] if (t in unigrams[0]) else 0 
            p_t = math.log((val + 1) / (unigrams[0]["total"] +  V))
        else:
            val1 = diagrams[0][prev + t] if ((prev + t) in diagrams[0]) else 0
            val2 = unigrams[0][prev] if (prev in unigrams[0]) else 0
            p_t = math.log((val1 + 1) / (val2 + V))
        p_e += p_t

    # french
    p_f = 1
    prev = ""
    V = len(unigrams[1]) - 1
    for t in text:
        p_t = 0
        # start
        t = t.lower()
        if prev == "":
            val = unigrams[1][t] if (t in unigrams[1]) else 0 
            p_t = math.log((val + 1) / ( unigrams[1]["total"] +  V))
        else:
            val1 = diagrams[1][prev + t] if ((prev + t) in diagrams[1]) else 0
            val2 = unigrams[1][prev] if (prev in unigrams[1]) else 0
            p_t = math.log((val1 + 1) / (val2 + V))
        p_f += p_t
    
    # italian
    p_i = 1
    prev = ""
    V = len(unigrams[2]) - 1
    for t in text:
        p_t = 0
        # start
        t = t.lower()
        if prev == "":
            val = unigrams[2][t] if (t in unigrams[2]) else 0 
            p_t = math.log((val + 1) / ( unigrams[2]["total"]  +  V))
        else:
            val1 = diagrams[2][prev + t] if ((prev + t) in diagrams[2]) else 0
            val2 = unigrams[2][prev] if (prev in unigrams[2]) else 0
            p_t = math.log((val1 + 1) / (val2 + V))
        p_i += p_t
    
    winner = max([p_e, p_f, p_i]) 
    if winner == p_e:
        return langs[0]
    if winner == p_f:
        return langs[1]
    return langs[2]





def main(testfile):
    directory = os.path.join('languageIdentification.data', 'training')
    e = open(os.path.join(directory, "English"), 'r', encoding="ISO-8859-1")
    f = open(os.path.join(directory, "French"), 'r', encoding="ISO-8859-1")
    i = open(os.path.join(directory, "Italian"), 'r', encoding="ISO-8859-1")

    # English
    e_uni = {}
    e_di = {}    
    Lines = e.readlines()
    for line in Lines:
        uni, di = trainBigramLanguageModel(line)
        for u in uni:
            if u in e_uni:
                e_uni[u] += uni[u]
            else:
                e_uni[u] = uni[u]
        for d in di:
            if d in e_di:
                e_di[d] += di[d]
            else:
                e_di[d] = di[d]

    # French
    f_uni = {}
    f_di = {}
    Lines = f.readlines()
    for line in Lines:
        uni, di = trainBigramLanguageModel(line)
        for u in uni:
            if u in f_uni:
                f_uni[u] += uni[u]
            else:
                f_uni[u] = uni[u]
        for d in di:
            if d in f_di:
                f_di[d] += di[d]
            else:
                f_di[d] = di[d]

    # Italian
    i_uni = {}
    i_di = {}
    Lines = i.readlines()   
    for line in Lines:
        uni, di = trainBigramLanguageModel(line)
        for u in uni:
            if u in i_uni:
                i_uni[u] += uni[u]
            else:
                i_uni[u] = uni[u]
        for d in di:
            if d in i_di:
                i_di[d] += di[d]
            else:
                i_di[d] = di[d]


    # Test
    langs = ["English", "French", "Italian"]
    t = open(testfile, 'r', encoding="ISO-8859-1")
    Lines = t.readlines()
    count = 1
    out_file = open("languageIdentificaton.output", "w")
    sys.stdout = out_file
    for line in Lines:
        language = identifyLanguage(line, langs, [e_uni, f_uni, i_uni], [e_di, f_di, i_di])
        # print(line + " " + language)
        print(str(count) + " " + language)
        count += 1



    
    





if __name__ == '__main__':

    main(sys.argv[1])