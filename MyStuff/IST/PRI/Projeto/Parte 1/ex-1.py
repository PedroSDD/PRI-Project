from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
import logging
logging.basicConfig()

def score_candidates(filename ):

    file_name = open(filename)
    train = fetch_20newsgroups(subset='train')
    vectorizer = TfidfVectorizer(use_idf=False, stop_words='english', ngram_range=(1, 2))
    train_vec = vectorizer.fit_transform(train.data)
    my_doc_tfidf = vectorizer.transform(file_name)

    feature_names = vectorizer.get_feature_names()
    dense = my_doc_tfidf.todense()
    densed_idf = dense[0].tolist()[0]
    scores = zip(range(0, len(densed_idf)), densed_idf)
    feature_sorted = sorted(scores, key=itemgetter(1))[-5:]

    feature_name_sorted = []

    for pair in feature_sorted:
        feature_name_sorted.append(feature_names[pair[0]])
    print feature_name_sorted
    return feature_name_sorted


def initializer():
    score_candidates('teste')


initializer()