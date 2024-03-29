import codecs
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
import logging
logging.basicConfig()

def read_files_text(path):
    content_all_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            content = codecs.open(os.path.join(path, file), encoding='utf-8', errors='replace')
            content_all_files.append(content.read().lower())
    return content_all_files


def score_candidates(filename, train):

    file_name = open(filename)
    vectorizer = TfidfVectorizer(use_idf=False, stop_words='english', ngram_range=(1, 3))
    vectorizer.fit_transform(train)
    my_doc_tfidf = vectorizer.transform(file_name)

    feature_names = vectorizer.get_feature_names()
    dense = my_doc_tfidf.todense()
    densed_idf = dense[0].tolist()[0]
    scores = zip(range(0, len(densed_idf)), densed_idf)
    feature_sorted = sorted(scores, key=itemgetter(1))[-5:]

    feature_name_sorted = []
    key_phrases_dic = {}

    for pair in feature_sorted:
        feature_name_sorted.append(feature_names[pair[0]])

    for word in feature_name_sorted:
        key_phrases_dic[word] = 0

    return key_phrases_dic

def phrases_spliter(filename):
    list_phrases = []
    with open(filename, 'r') as file:
        all_phrases = file.read().strip().split('.')

        for words in all_phrases:
            list_phrases.append(words.split())
        return list_phrases

def generate_graph(all_edges_list):
    graph = {}
    edges_list=[]

    for line in all_edges_list:
        edges_list = line

        for value in edges_list:
            if value not in graph:
                for other_value in edges_list:
                    if value != other_value:
                        graph.setdefault(value, []).append(other_value)

            if value in graph:
                for other_value in edges_list:
                    if other_value not in graph[value] and value != other_value:
                        graph.setdefault(value, []).append(other_value)

    return graph


def create_graph(list_phrases, key_phrases_dic):
    graph = {}
    list_keywords_phrase = []
    all_edges_list = []

    for phrase in list_phrases:

        sentence = [x.lower() for x in phrase]
        bigrams = zip(sentence, sentence[1:])
        trigrams = zip(sentence, sentence[1:], sentence[2:])

        for word in sentence:
            if word in key_phrases_dic:
                list_keywords_phrase.append(word)

        for j in bigrams:
            big_str = j[0] + ' ' + j[1]
            if big_str in key_phrases_dic:
                list_keywords_phrase.append(big_str)

        for i in trigrams:
            trig_str = i[0] + ' ' + i[1] + ' ' + i[2]
            if trig_str in key_phrases_dic:
                list_keywords_phrase.append(trig_str)

        all_edges_list.append(list_keywords_phrase)
        list_keywords_phrase = []

    graph = generate_graph(all_edges_list)

    return graph

def pageRank(grafo, d, l):
    resultado = {}
    invertido = {}
    for key, value in grafo.iteritems():

        if key not in invertido.keys():
            invertido[key] = []
        for reference in value:
            if reference not in invertido.keys():
                invertido[reference] = []
            invertido[reference].append(key)

    numPages = len(grafo)
    for key, value in grafo.iteritems():
        resultado[key] = 1/(numPages*1.0)

    N = (numPages*1.0)
    for times in range(1, l+1):
        anterior = resultado.copy()
        for page in resultado.keys():

            somatorio = 0
            for reference in grafo[page]:
                v = anterior[reference] / (len(invertido[reference])*1.0)
                somatorio += anterior[reference]/(len(invertido[reference])*1.0)
            resultado[page] = (1-d) * 1.0 / N + d * somatorio
    print resultado
    return resultado


def initializer():
    train_data=read_files_text('NLM_500/documents/')
    key_phrase_dic = score_candidates('10933267.txt', train_data)
    list_phrases = phrases_spliter('10933267.txt')
    graph = create_graph(list_phrases, key_phrase_dic)
    pageRank(graph, 0.15, 49)

initializer()