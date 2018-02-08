from lib.utils_cs276 import *
import pandas

A = corpus_cs276(1)
print("QUESTION 1: Nombre de tokens dans CS276: %i" % A.length_tokens)
print("QUESTION 2: Taille du vocabulaire : %i" % A.length_voc)
B = corpus_cs276(2)

b_estim = math.log(float(A.length_voc)/float(B.length_voc))/math.log(float(A.length_tokens)/float(B.length_tokens))
k_estim = A.length_voc/math.pow(A.length_tokens,b_estim)
print("Valeur de b estimee:  %.04f" % b_estim)
print("Valeur de k estimee: %i" %k_estim)

vocabulary_size_1m = k_estim * math.pow(1000000,b_estim)

print("QUESTION 4: Si on a 1 million de tokens, on peut estimer la taille du vocabulaire a %i " % int(vocabulary_size_1m))
# Creation of an inversed index using Map Reduce paradigm
print("Creation of an inversed index on the corpus using the MAP REDUCE paradigm")
index_inverse = A.map_reduce_index()
