import re, math,collections,nltk
import matplotlib.pylab as plt
import pandas
from lib.utils_CACM import *
from lib.boolean_motor import *

print("#########  Recherche Booléenne dans le corpus CACM ###############")
A = corpus_CACM(SHOW_GRAPH=False)
index_inv = A.create_index()

query = input("Que cherchez-vous ? (format attendu sous la forme normale conjonctive: a|b&c)")
print(moteur_bool(query,A.dic_termes,A.dic_docs,A.index_inv))
