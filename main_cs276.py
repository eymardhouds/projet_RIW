from lib.utils_cs276 import *
import pandas

A = corpus_cs276(1)
# question 1
print(A.length_tokens)
# question 2
print(A.length_voc)
# question 3
B = corpus_cs276(2)
print(B.length_tokens)
print(B.length_voc)
b_estim = math.log(float(A.length_voc)/float(B.length_voc))/math.log(float(A.length_tokens)/float(B.length_tokens))
k_estim = A.length_voc/math.pow(A.length_tokens,b_estim)
print(b_estim)
print(k_estim)
# question 4
vocabulary_size_1m = k_estim * math.pow(1000000,b_estim)
print(int(vocabulary_size_1m))
# question 5

# Creation of an inversed index using Map Reduce
A.map_reduce_index()
