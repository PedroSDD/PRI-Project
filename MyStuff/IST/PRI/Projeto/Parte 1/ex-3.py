import nltk
import codecs
import os
from sklearn.feature_extraction.text import CountVectorizer
import logging

logging.basicConfig()


def candidate_selector(filename):
    file_name = codecs.open(os.path.join('NLM_500/documents/', filename), encoding='utf-8', errors='replace')
    v = CountVectorizer(ngram_range=(1, 3), stop_words='english')
    words_vec = v.fit(file_name).vocabulary_
    return words_vec

def tri_grams(tag_list, noum):
    J = 'JJ'
    I = 'IN'
    Noum = 'NN'
    if J and Noum and I in tag_list:
        return True
    if J and Noum in tag_list and noum == 2:
        return True
    if noum == 3 :
        return True
    return False

def bi_grams (tag_list, noum) :
    J = 'JJ'
    I = 'IN'
    Noum = 'NN'
    if J and Noum in tag_list:
        return True
    if noum == 2:
        return True
    if Noum and I in tag_list:
        return True
    return False

def check_tag(words):
    tag_list=[]
    noum=0
    Noum='NN'
    out= False

    for i in range(len(words)):
        tag_list.append(words[i][1])
        if words[i][1] == Noum :
            noum += 1
    if noum == 0:
        return False
    if len(words)==3:
        out=tri_grams(tag_list, noum)
    if len(words)==2:
        out=bi_grams(tag_list, noum)
    if len(words)==1 and Noum in tag_list:
        return True

    return out

def candidates_filter(list_of_ngrams):
    keys = list_of_ngrams.keys()
    list_filtered_words = []
    d = 0
    for i in keys:
        sentence = keys[d].split()
        taggers = nltk.pos_tag(sentence)
        if check_tag(taggers) and sentence not in list_filtered_words:
               list_filtered_words.append(sentence)
        d += 1

    return list_filtered_words

def initializer():
    for file in os.listdir('NLM_500/documents/'):
        if file.endswith(".txt"):
            candidates = candidate_selector(file)
            candidates_true=candidates_filter(candidates)
            print (' For file' + file + 'we get: ' + candidates_true)

initializer()