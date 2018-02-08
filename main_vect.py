import re, math,collections,nltk
import matplotlib.pylab as plt
import pandas,time
from lib.utils_CACM import *
from lib.vect_motor import *
from nltk.tokenize import sent_tokenize, word_tokenize,RegexpTokenizer


print("\n\n#########  Recherche vectorielle dans le corpus CACM  ###############\n")
print("Initialisation et analyse du corpus...merci de patienter")
start=time.time()
A = corpus_CACM(SHOW_GRAPH=False)
index_inv = A.create_index_inv()
index=A.create_index()
end=time.time()
timer_index= end-start
print("Indexation en %0.01f sec" % timer_index)
tokenizer = RegexpTokenizer(r'\w+')

do_research=1
while do_research!=0:
    method = input("Quelle methode souhaitez-vous utiliser pour la recherche vectorielle ? (tf_idf,ntf_idf,maxfreq)")
    query = input("Que cherchez-vous ? (une liste de mots)")

    query=tokenizer.tokenize(query)

    result,timer = moteur_vect(method,query,A.t_id_term,A.index,A.dic_termes,A.dic_docs,A.index_inv,A.tokens,10)
    print("\n \n ############ TOP 10 RELEVANT WORK FOUND IN CACM in %0.01f sec ###################### \n" % timer)
    for doc_id in result:
        print(A.dic_docs[doc_id])
    print("\n\nVous pouvez effectuer une nouvelle recherche\n\n###############################\n\n")
