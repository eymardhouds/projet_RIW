import collections
import math,time
from nltk.tokenize import sent_tokenize, word_tokenize,RegexpTokenizer

def get_tf_df(word_id,doc_id,dic_docs,tokens_count_by_doc_id):
    if tokens_count_by_doc_id[(word_id,doc_id)]!=0:
        tf=1+math.log(tokens_count_by_doc_id[(word_id,doc_id)],10)
        idf=math.log(len(dic_docs)/tokens_count_by_doc_id[(word_id,doc_id)],10)
        tf_idf=tf*idf
    else:
        tf_idf=0
    return tf_idf

def get_tf_df_normalized(word_id,doc_id,dic_docs,tokens_count_by_doc_id):
    if tokens_count_by_doc_id[(word_id,doc_id)]!=0:
        tf=1+math.log(tokens_count_by_doc_id[(word_id,doc_id)],10)
        idf=math.log(len(dic_docs)/tokens_count_by_doc_id[(word_id,doc_id)],10)
    if tf != 0:
        n_tf = 1 + math.log(tf, 10)
        n_tf_idf= n_tf*idf
    else:
        n_tf_idf=0

    return n_tf*idf

def get_max_freq(term_id,doc_id,dic_docs,tokens_count_by_doc_id,mf):
    max_tf = mf[doc_id]
    mtf=0
    if tokens_count_by_doc_id[(word_id,doc_id)]!=0:
        mtf=mtf+1
    if max_tf==0:
        return 0
    return mtf/max_tf

def cos_measure(index,doc_id,query_weights,query_cos_square,tokens_count_by_doc_id,dic_docs,method,mf):
    sum_cos_square=0
    sum_cos=0

    for term in index[doc_id]:
        if method="tf_idf":
            weight_tid_doc_id = get_tf_id(term,doc_id,dic_docs,tokens_count_by_doc_id)
        elif method="ntf_idf":
            weight_tid_doc_id = get_tf_df_normalized(term,doc_id,dic_docs,tokens_count_by_doc_id)
        elif method="maxfreq":
            weight_tid_doc_id = get_max_freq(term,doc_id,dic_docs,tokens_count_by_doc_id,mf)

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

    if method=="tf_idf" or method=="ntf_idf":
        for query_component in query:
            query_component=query_component.lower()
            if query_component in dic_termes.keys():
                if dic_termes[query_component] in index_inv.keys():
                    index_inv[dic_termes[query_component]].append(-99)
                tokens.append((dic_termes[query_component],-99))

    elif method="maxfreq":
        # ICI MODIFIER

    # Retun a dic : {(word,doc_id) : n times} to say that a word occured n times in doc_id
    tokens_count_by_doc_id = collections.Counter(tokens)

    mf = max_freq(index_inv,dic_docs,dic_termes)

    # We need to compute info about the query first
    for term_id in t_id_term:
        if method == "tf_idf":
            query_weights[term_id] = get_tf_idf(term_id,-99,dic_docs,tokens_count_by_doc_id)
        elif method="ntf_idf":
            query_weights[term_id] = get_tf_df_normalized(term_id,-99,dic_docs,tokens_count_by_doc_id)
        elif method="maxfreq":
            query_weights[term_id]=get_max_freq(term_id,-99,dic_docs,tokens_count_by_doc_id,mf)
        query_cos_square = query_cos_square+query_weights[term_id]**2

    for doc_id in index:
        cos_factor.append((doc_id,cos_measure(index,doc_id,query_weights,query_cos_square,tokens_count_by_doc_id,dic_docs,method,mf)))

    end = time.time()
    res = sorted(cos_factor,key=lambda m: m[1],reverse=True)
    return res[:nbr_ret],end-start

def max_freq(index_inv,dic_docs,dic_termes):
    # Get by doc id the max frequency
    max_freq={}
    for d in range(len(dic_docs)):
        max_freq[d]=0
        for t in range(len(dic_termes)):
            count=0
            for dbis in index_inv[t]:
                if dbis==d:
                count=count+1
                if max_freq[d]<count:
                    max_freq[d]=count
    return max_freq
