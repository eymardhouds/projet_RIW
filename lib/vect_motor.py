import collections
import math,time
from nltk.tokenize import sent_tokenize, word_tokenize,RegexpTokenizer

def get_weights_word(word_id,doc_id,dic_docs,tokens_count_by_doc_id):
    if tokens_count_by_doc_id[(word_id,doc_id)]!=0:
        tf=1+math.log(tokens_count_by_doc_id[(word_id,doc_id)],10)
        idf=math.log(len(dic_docs)/tokens_count_by_doc_id[(word_id,doc_id)],10)
        tf_idf=tf*idf
    else:
        tf_idf=0
    return tf_idf

def cos_measure(index,doc_id,query_weights,query_cos_square,tokens_count_by_doc_id,dic_docs):
    sum_cos_square=0
    sum_cos=0

    for term in index[doc_id]:
        weight_tid_doc_id = get_weights_word(term,doc_id,dic_docs,tokens_count_by_doc_id)
        sum_cos = sum_cos + query_weights[term]*weight_tid_doc_id
        sum_cos_square =sum_cos_square + weight_tid_doc_id**2

    if sum_cos_square!=0 or query_cos_square!=0:
        res = sum_cos/(sum_cos_square+query_cos_square)
    else:
        res=0
    return res

def moteur_vect(method,query,t_id_term,index,dic_termes,dic_docs,index_inv,tokens,nbr_ret):
    start = time.time()
    query_weights = {}
    query_cos_square=0
    cos_factor=[]
    t_id_doc_id = []
    tokenizer = RegexpTokenizer(r'\w+')

    for query_component in query:
        query_component=query_component.lower()
        if query_component in dic_termes.keys():
            if dic_termes[query_component] in index_inv.keys():
                index_inv[dic_termes[query_component]].append(-99)
            tokens.append((dic_termes[query_component],-99))

    # Retun a dic : {(word,doc_id) : n times} to say that a word occured n times in doc_id
    tokens_count_by_doc_id = collections.Counter(tokens)
    if method == "tf_idf":
        # We need to compute info about the query first
        for term_id in t_id_term:
            query_weights[term_id] = get_weights_word(term_id,-99,dic_docs,tokens_count_by_doc_id)
            query_cos_square = query_cos_square+query_weights[term_id]**2

        for doc_id in index:
            cos_factor.append((doc_id,cos_measure(index,doc_id,query_weights,query_cos_square,tokens_count_by_doc_id,dic_docs)))
    else:
        print("Pas encore d'autres methodes")
    end = time.time()
    res = sorted(cos_factor,key=lambda m: m[1],reverse=True)
    return res[:nbr_ret],end-start
