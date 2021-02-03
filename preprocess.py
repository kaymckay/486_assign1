"""Kayla McKay (kaymckay)"""

import sys
import os
import re
from stemmer import PorterStemmer

def removeSGML(line):
    """Function that removes SGML tags. """
    # data = re.sub(r'<.*?>', '', line)
    tag = False
    quote = False
    cleanedLine = ""

    for char in line:
        if char == '<' and not quote:
            tag = True
        elif char == '>' and not quote:
            tag = False
        elif (char == '"' or char == "'") and tag:
            quote = not quote
        elif not tag:
            cleanedLine = cleanedLine + char 

    # print(cleanedLine)
    return cleanedLine


def tokenizeText(line):
    """Function that tokenizes the text. """
    # initial split
    line = line.strip('\n')
    line = decontract(line)
    # print(line)
    line = line.split(' ')
    tokens = []

    # check for cases
    token = ""
    first = ""
    second = ""
    for word in line:
        if not word == '':
            # print(word)
            for w in word:
                # acronyms/abbreviatons
                if  w == '.':
                    if first == 'period':
                        token = token[: len(token) - 1]
                        tokens.append(token)
                        token = '..'
                        first, second = 'period', first
                    elif first == 'cap' or first == "" or first == 'letter':
                        token += w
                        first, second = 'period', first
                    elif first == "num":
                        if w == word[len(word) - 1]:
                            tokens.append(token)
                            token = "."
                        else:   
                            token += w
                            first, second = 'period', first
                elif w == ',':
                    if first == 'num':
                        if w == word[len(word) - 1]:
                            tokens.append(token)
                            token = ","
                        else:
                            token += w
                            first, second = 'comma', first
                    else:
                        tokens.append(token)
                        tokens.append(',')
                        token = ""
                elif w == "'":
                    tokens.append(token)
                    token = "'"
                    first, second = 'apos', ""
                elif w.isupper():
                    token += w.lower()
                    first, second = 'cap', first
                elif w == '/':
                    if first == 'num':
                        token += w
                        first, second = 'slash', first
                    elif first == "":
                        tokens.append('/')
                        first, second = "", ""
                    elif first == "letter":
                        tokens.append(token)
                        token = ""
                        tokens.append('/')
                        first, second = 'slash', ""
                elif w == '-':
                    if first == 'letter' or first == 'num':
                        token += w
                        first, second = 'dash', first
                    elif first == 'period':
                        tokens.append(token)
                        token = w
                        first, second = 'dash', ""
                    elif first == 'dash':
                        token += w
                        first, second = 'dash', first
                elif w == '(':
                    if first == 'letter' or first == 'num':
                        token += w
                        first, second = 'para1', first
                    else:
                        tokens.append('(')
                elif w == ')':
                    if second == 'para1':
                        token += w
                        first, second = 'para2', first
                    else:
                        tokens.append(token)
                        token = ""
                        tokens.append(')')
                elif w.isdigit():
                    token += w
                    first, second = 'num', first
                else:
                    if second == 'dash' and first == 'dash':
                        tokens.append(token)
                        token = w
                        first, second = 'letter', ""
                    else:
                        token += w
                        first, second = 'letter', first

            if not token == "":
                tokens.append(token)
            first = ""
            second = ""
            token = ""
    
    # print(tokens)
    return tokens


    # return list

def decontract(line):
    contractions = {
        "ain't": "am not / are not",
        "aren't": "are not / am not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "I would",
        "i'd've": "I would have",
        "i'll": "I will",
        "i'll've": "I will have",
        "i'm": "I am",
        "i've": "I have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "iit will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have"
    }
    
    for word in line.split():
        if word.lower() in contractions:
                line = line.replace(word, contractions[word.lower()])

    return line





def removeStopwords(tokens):
    """Function that removes the stopwords. """

    tokens = [word for word in tokens if word not in stopwords]
    
    return tokens
    

def stemWords(tokens):
    """Function that stems the words. """
    # use porter stemmer 
    #  https://tartarus.org/martin/PorterStemmer/python.txt

    p = PorterStemmer()
    for index, word in enumerate(tokens):
        tokens[index] = p.stem(word, 0, len(word) - 1)

    return tokens



stopwords = []

def main(directory):
    """Main functon."""

    s = open('stopwords', 'r')
    Words = s.readlines()
    for w in Words:
        stopwords.append(w.strip('\n'))

    global_tokens = {}

    # go through every file in directory provided
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f: 
            Lines = f.readlines()
            for line in Lines:
                line = removeSGML(line)
                tokens = tokenizeText(line)
                if tokens:
                    tokens = removeStopwords(tokens)
                    tokens = stemWords(tokens)
                    for token in tokens:
                        if token in global_tokens:
                            global_tokens[token] += 1
                        else:
                            global_tokens[token] = 1
    

    # Get stats on collection
    total_num = 0
    total_unique = 0

    for token in global_tokens:
        if any(c.isalpha() for c in token) or any(c.isdigit() for c in token):
            # if token.isalpha() or token.isdigit():
            total_num += global_tokens[token]
            total_unique += 1

    global_tokens = sorted(global_tokens.items(), key=lambda kv: kv[1], reverse=True)
    top_50 = []
    for token in global_tokens:
        if token[0].isalpha() or token[0].isdigit():
            top_50.append(token)
        if len(top_50) == 50:
            break
    
    out_file = open("preprocess.output", "w")
    sys.stdout = out_file
    print("Words " + str(total_num))
    print("Vocabulary " + str(total_unique))
    print("Top 50 words")


    for token in top_50:
        print(str(token[0]) + " " + str(token[1]))







# def subset(directory):
#     global_tokens = {}

#     with open(os.path.join(directory, "cranfield0011"), 'r') as f: 
#             Lines = f.readlines()
#             for line in Lines:
#                 line = removeSGML(line)
#                 tokens = tokenizeText(line)
#                 if tokens:
#                     tokens = removeStopwords(tokens)
#                     tokens = stemWords(tokens)
#                     for token in tokens:
#                         if token in global_tokens:
#                             global_tokens[token] += 1
#                         else:
#                             global_tokens[token] = 1

#     # Get stats on collection
#     total_num = 0
#     total_unique = 0

#     for token in global_tokens:
#         if any(c.isalpha() for c in token) or any(c.isdigit() for c in token):
#             # if token.isalpha() or token.isdigit():
#             total_num += global_tokens[token]
#             total_unique += 1

#     global_tokens = sorted(global_tokens.items(), key=lambda kv: kv[1], reverse=True)


#     print("Words " + str(total_num))
#     print("Vocabulary " + str(total_unique))

#     global_tokens = {}
#     with open(os.path.join(directory, "cranfield0037"), 'r') as f: 
#         Lines = f.readlines()
#         for line in Lines:
#             line = removeSGML(line)
#             tokens = tokenizeText(line)
#             if tokens:
#                 tokens = removeStopwords(tokens)
#                 tokens = stemWords(tokens)
#                 for token in tokens:
#                     if token in global_tokens:
#                         global_tokens[token] += 1
#                     else:
#                         global_tokens[token] = 1
    

#     # Get stats on collection
#     total_num = 0
#     total_unique = 0

#     for token in global_tokens:
#         if any(c.isalpha() for c in token) or any(c.isdigit() for c in token):
#             # if token.isalpha() or token.isdigit():
#             total_num += global_tokens[token]
#             total_unique += 1

#     global_tokens = sorted(global_tokens.items(), key=lambda kv: kv[1], reverse=True)


#     print("Words " + str(total_num))
#     print("Vocabulary " + str(total_unique))




if __name__ == '__main__':
    # run main
    # python3 preprocess.py cranfieldDocs
    main(sys.argv[1])
    # subset(sys.argv[1])