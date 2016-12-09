import os
import feedparser
import logging
import codecs
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
logging.basicConfig()


global rss_feeds


def get_rss_notices(url):
    print "A obter noticias de ", url

    rss = feedparser.parse(url)

    for notice in rss['entries']:
        title = notice.title
        description = notice.description
        f = codecs.open("notices.txt", "w", encoding='utf-8', errors='replace')
        f.write(title)
        f.write(description)
        f.close()

def score_candidates(filename):

    file_name = open(filename)
    train = fetch_20newsgroups(subset='train')
    vectorizer = TfidfVectorizer(use_idf=False, stop_words='english', ngram_range=(1, 2))
    train_vec = vectorizer.fit_transform(train.data)
    my_doc_tfidf = vectorizer.transform(file_name)

    feature_names = vectorizer.get_feature_names()
    dense = my_doc_tfidf.todense()
    densed_idf = dense[0].tolist()[0]
    scores = zip(range(0, len(densed_idf)), densed_idf)
    feature_sorted = sorted(scores, key=itemgetter(1))[-20:]

    feature_name_sorted = []

    for pair in feature_sorted:
        feature_name_sorted.append(feature_names[pair[0]])

    for keyphrase in feature_name_sorted:
        keyphrases_file = codecs.open("keyphrases.txt", "a", encoding='utf-8', errors='replace')
        keyphrases_file.write('\n' + keyphrase)
        keyphrases_file.close()

    contents = codecs.open("keyphrases.txt", encoding='utf-8', errors='replace')
    with codecs.open("keyphrases.html", "a", encoding='utf-8', errors='replace') as e:
        for lines in contents.readlines():
            e.write("<pre>" + lines + "</pre> <br>\n")
    return feature_name_sorted


get_rss_notices("http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
score_candidates("notices.txt")

