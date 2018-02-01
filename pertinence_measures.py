
from lib.utils_CACM import *
from lib.vect_motor import *
from lib.utils_pertinence import *
import matplotlib.pylab as plt
import time


if __name__ == '__main__':
    results ={}
    duration={}
    total_d=0
    commonwords=get_commonwords()
    queries = parser_queries_text(commonwords)
    q_res = parser_queries_results(queries)
    print("################ Corpus analysis #################")
    corpus_start=time.time()
    A = corpus_CACM(SHOW_GRAPH=False)
    index_inv = A.create_index_inv()
    index = A.create_index()
    corpus_end=time.time()
    corpus_time = corpus_end-corpus_start
    print("Corpus analyzed and indexed in %.03f secs" % corpus_time)

    print("################# Queries ####################")
    for q in q_res:
        print("Calcul en cours de " + str(q)+"/"+str(len(q_res)))
        q_word = queries[q]
        results[q],duration[q] = moteur_vect("tf_idf",q_word,A.t_id_term,A.index,A.dic_termes,A.dic_docs,A.index_inv,A.tokens,3203)
    for d in duration:
        duree=duration[d]
        total_d=duree+total_d
    avg_duree = total_d/len(duration)

    print("##########  Duree moyenne de %.02f ####################" % avg_duree)

    print("######## Precision and Rappel computation #############")
    print("Computing precision and rappel")
    precision,rappel = get_rappel_and_precision(results,q_res,A.dic_docs)
    print("e and f measures")
    e_measures,f_measures=get_f_e_measures(precision,rappel,A.dic_docs,q_res)
    print("plotting")
    plot_precision_rappel(precision,rappel,A.dic_docs,q_res)
