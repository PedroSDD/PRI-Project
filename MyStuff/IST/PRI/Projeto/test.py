import codecs
import os

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
import logging
logging.basicConfig()


def read_files_text(path):
    content_all_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            content = codecs.open(os.path.join(path, file), encoding='utf-8', errors='replace')
            content_all_files.append(content.read())
    return content_all_files



def score_candidates(path, filename, vectorizer):
    file_name = codecs.open(filename, encoding='utf-8', errors='replace')

    test_vec = vectorizer.transform(file_name)

    feature_names = vectorizer.get_feature_names()
    dense = test_vec.todense()
    densed_idf = dense[0].tolist()[0]
    scores = zip(range(0, len(densed_idf)), densed_idf)
    feature_sorted = sorted(scores, key=itemgetter(1))[-20:]

    feature_name_sorted = []
    for pair in feature_sorted:
        feature_name_sorted.append(feature_names[pair[0]])
    print feature_name_sorted
    return feature_name_sorted


def get_key_values(file):
    content_all_files = []
    content = codecs.open(file, encoding='utf-8', errors='replace')
    for line in content.readlines():
        content_all_files.append(line.lower().split('\n')[0])
    return content_all_files


def precision(retrieved, relevant):
    return "Precision: ", float((len(list(set(retrieved) & set(relevant))))) / float((len(retrieved)))


def recall(a, r):
    return "Recall: ", float((len(set(iter(a)) & set(iter(r))))) / float((len(r)))


def f1(pr, re):
    return "f1 score: ", float(((2 * re * pr) / (re + pr)))

from os import walk

def list_filenames():
    f = []
    for (dirpath, dirnames, filenames) in walk('NLM_500/documents'):
        f.extend(filenames)
    return f

def initializer():
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    vectorizer.fit_transform(read_files_text('NLM_500/documents/'))
    pr_mean = []
    for name in list_filenames():
        if '.key' in name:
            r = get_key_values('NLM_500/documents/' + name)
            name = name[:-3] + 'txt'
            a = score_candidates('NLM_500/documents', 'NLM_500/documents/' + name, vectorizer)
            pr = precision(a, r)
            #recall e f1
            print(pr)
            pr_mean += [pr]
    temp = 0
    for val in pr_mean:
        temp += val
    print('Mean Precision', temp/len(pr_mean))
    # re = recall(a, r)
    # f1(pr, re)

initializer()