
import re, math,collections,nltk
import matplotlib.pylab as plt
import pandas,time
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize,RegexpTokenizer

class corpus_CACM:
    def __init__(self,SHOW_GRAPH):
        self.common_words = self.get_commonwords()
        self.dic_docs,self.tokens,self.dic_termes= self.tokenization()
        self.SHOW_GRAPHS = SHOW_GRAPH

    def get_commonwords(self):
        with open('data/CACM/common_words','r') as doc:
            content = doc.readlines()
        common_words = [x.strip() for x in content]
        return common_words

    def tokenization(self):
        #.I, .T, .W et .K.
        """
        Return a dic with words that have been seen and parsed by article ids
        """
        with open('data/CACM/cacm.all','r') as doc:
            t_time=time.time()
            content = doc.readlines()
            content = [x.strip() for x in content]
            self.dic_docs={}
            self.dic_termes={}
            self.tokens=[]
            tokenizer = RegexpTokenizer(r'\w+')
            nbr=0
            i=0
            current_id=0
            # nombre total de lignes #content_stringified = ' '.join(content) #last_id_position = content_stringified.rfind(".I") #last_article_id = int(content_stringified[last_id_position+2:last_id_position+7])
            while current_id < 3203:
                j=0 # nombre de lignes dans un article
                if content[i+j][:2] == ".I":
                    current_id = int(content[i+j][2:])
                    j =j+1
                    while content[i+j][:2]!=".I":
                        if content[i+j] == ".W" or content[i+j] == ".K" or content[i+j] == ".T":
                            if content[i+j] == ".T":
                                j=j+1
                                self.dic_docs[current_id] = content[i+j]
                            j=j+1
                            while content[i+1+j][0]!=".":
                                listwords = tokenizer.tokenize(content[i+j])
                                listwords=[r.lower() for r in listwords]
                                for r in listwords:
                                    if r not in self.dic_termes:
                                        self.dic_termes[r]=nbr
                                        nbr=nbr+1
                                    self.tokens.append((self.dic_termes[r],current_id))
                                j=j+1
                        j=j+1
                i=i+j
        e_time = time.time()
        print("TOKENIZATION " + str(e_time-t_time))
        self.t_id_term()
        return self.dic_docs,self.tokens,self.dic_termes

    def t_id_term(self):
        self.t_id_term={}
        for key in self.dic_termes:
            self.t_id_term[self.dic_termes[key]]=key
        return self.t_id_term

    def get_vocabulary(self,tokens):
        g_time=time.time()
        already_seen=[]
        vocabulary=[]
        for token in tokens:
            if token[0] not in already_seen and self.t_id_term[token[0]] not in self.common_words and self.t_id_term[token[0]] not in stopwords.words('english'):
                vocabulary.append(token)
                already_seen.append(token[0])
        k_time=time.time()
        print("VOCA " + str(k_time-g_time))
        return vocabulary

    def create_index(self):
        l_time=time.time()
        self.index={}
        for k in self.tokens:
            if k[1] not in self.index:
                self.index[k[1]]=[]
            self.index[k[1]].append(k[0])
        v_time=time.time()
        print("INDEX " + str(v_time-l_time))
        return self.index

    def create_index_inv(self):
        l_time=time.time()
        self.index_inv={}
        for k in self.tokens:
            if k[0] not in self.index_inv:
                self.index_inv[k[0]]=[]
            self.index_inv[k[0]].append(k[1])
        v_time=time.time()
        print("INDEX INV " + str(v_time-l_time))
        return self.index_inv

    def zipf_verification(self):
        tokens = self.tokens
        for word in tokens:
            if self.dic_termes.keys()[self.dic_termes.values().index(word)] in self.common_words:
                 tokens.remove(word)
        count_zipf = nltk.FreqDist(self.tokens).most_common()
        count_zipf.sort(key=lambda t: t[1], reverse=True)
        ranks=[]
        freq=[]
        for r, f in enumerate(count_zipf):
            ranks.append(r)
            freq.append(f[1])
        #count_zipf_df=count_zipf_df.set_index('rank')
        if self.SHOW_GRAPHS:
            plt.figure(1)
            plt.subplot(211)
            plt.title('f en fonction de r')
            plt.plot(ranks, freq)
            log_ranks = [math.log(rank + 1) for rank in ranks]
            log_frequencies = [math.log(frequency) for frequency in freq]
            plt.subplot(212)
            plt.title('logarithmes')
            plt.plot(log_ranks, log_frequencies)
            plt.show()
        return count_zipf

    def get_b_k(self):
        tokens_A = self.tokens
        tokens_B = self.tokens[:len(self.tokens)/2]
        vocabulary_size_A_with_doc_id = float(len(self.get_vocabulary(tokens_A)))
        vocabulary_size_B_with_doc_id = float(len(self.get_vocabulary(tokens_B)))
        count_token_A = float(len(tokens_A))
        count_token_B = float(len(tokens_B))
        self.b_estim = math.log(vocabulary_size_B_with_doc_id/vocabulary_size_A_with_doc_id)/math.log(count_token_B/count_token_A)
        self.k_estim = vocabulary_size_A_with_doc_id/math.pow(count_token_A,self.b_estim)
        self.vocabulary_size_4 = self.k_estim * math.pow(1000000,self.b_estim)
        return self.b_estim, self.k_estim
