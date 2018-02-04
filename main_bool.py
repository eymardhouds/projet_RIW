import re, math,collections,nltk
import matplotlib.pylab as plt
import pandas,time
from lib.utils_CACM import corpus_CACM
from lib.boolean_motor import moteur_bool

print("#########  Recherche Booleenne dans le corpus CACM ###############")

A = corpus_CACM(SHOW_GRAPH=False)
index_inv = A.create_index_inv()
cherche=1

while cherche==1:
    query = input("Que cherchez-vous ? (format attendu sous la forme normale conjonctive: a|b&c)")
    start=time.time()
    res=moteur_bool(query,A.dic_termes,A.dic_docs,index_inv)
    end=time.time()

    timer= end-start

    print("\n \n ############ RELEVANT WORK FOUND IN CACM in %0.05f sec ###################### \n" % timer)
    for doc_id in res:
        print(A.dic_docs[doc_id])
    print("\n\nVous pouvez effectuer une nouvelle recherche\n\n###############################\n\n")
