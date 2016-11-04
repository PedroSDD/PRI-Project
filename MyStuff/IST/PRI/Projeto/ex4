import codecs
import os
import string

import math
import nltk
import numpy



def file_cleaner(file):
    content_all_files = []
    content = codecs.open(file, encoding='utf-8', errors='replace')
    for line in content.readlines():
        line = "".join(ch for ch in line if ch not in set(string.punctuation))
        tokens = nltk.word_tokenize(line)
        tokens = ' '.join(tokens)
        for word in tokens.split(" "):
            content_all_files.append(word)
    return content_all_files

def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def create_ngram_dictionary(n_gram_generated):
    dictionary_n_gram = {}
    for n_gram in n_gram_generated:
        if n_gram not in dictionary_n_gram:
            dictionary_n_gram[n_gram] = 1
        else:
            dictionary_n_gram[n_gram] += 1
    return dictionary_n_gram

def n_grams_filtered(file_clean, n):
    return find_ngrams(file_clean, n)

def calc_prob(file_clean, n, n_gram):
    count = 0
    for word in file_clean:
        if word == n_gram:
            count += 1

    if n == 1:
        produt = count / float(len(file_clean))
        return produt


def sigma_calculator(pw, qw):
    print "Valor do sigma e :",  pw * math.log(pw/qw)
    return pw * math.log(pw, qw)


def initializer():
    input_list_clean = file_cleaner('testeex4')
    pw = calc_prob(input_list_clean, 1, "is")
    qw = calc_prob(input_list_clean, 1, "is")
    print "O valor do pw: ", pw
    print "O valor do qw: ", qw
    lmfg = sigma_calculator(pw, qw)
    print "O valor do lmfg: ", lmfg

initializer()