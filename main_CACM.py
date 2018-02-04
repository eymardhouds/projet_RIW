import re, math,collections,nltk
import matplotlib.pylab as plt
import pandas
from lib.utils_CACM import *
from lib.boolean_motor import *

# *********** AFFICHAGE DES REPONSES AUX QUESTIONS ********************************
A = corpus_CACM(SHOW_GRAPH=True)

print("QUESTION 1: Nombre de tokens dans CACM: %i" % len(A.tokens))
voc = A.get_vocabulary(A.tokens)
print("QUESTION 2: Taille du vocabulaire : %i" % len(voc))
print("QUESTION 3")
A.get_b_k()
print("Valeur de b estimee:  %.04f" % A.b_estim)
print("Valeur de k estimee: %i" %A.k_estim)
print("QUESTION 4: Si on a 1 million de tokens, on peut estimer la taille du vocabulaire a %i " % A.vocabulary_size_4)
print("QUESTION 5: Chargement des graphs")
A.zipf_verification()
print("Graphs affiches ")
