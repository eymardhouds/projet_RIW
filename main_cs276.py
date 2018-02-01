from lib.utils_CS276 import *
import pandas

A = corpus_cs276(1)
B = corpus_cs276(2)
# question 1
print(B.length_tokens)
# question 2
print(B.length_voc)
# question 3
b_estim = math.log(B.length_voc/A.length_voc)/math.log(B.length_tokens/A.length_tokens)
k_estim = A.length_voc/math.pow(A.length_tokens,b_estim)
print(b_estim)
print(k_estim)
# question 4
vocabulary_size_1m = k_estim * math.pow(1000000,b_estim)
print(vocabulary_size_1m)
# question 5
