# Stanford: Tokens: 25 000 000 et taukke 400 000
import re,math, os, collections,sys,time
from nltk.tokenize import sent_tokenize, word_tokenize
from multiprocessing import Manager, Pool


class corpus_cs276:

    def __init__(self,nbr_of_folders):
        self.nbr_of_folders=nbr_of_folders
        self.tokens,self.dic_docs,self.dic_termes = self.traitement_corpus() #C'est un grand tableau de tuples (term_id,doc_id)
        self.length_tokens = len(self.tokens)
        self.vocabulary = collections.Counter(x[0] for x in self.tokens)
        self.length_voc = len(self.vocabulary)

    def traitement_corpus(self):
        """
        Cette fonction renvoie:
        - une liste de tuples (word_id,doc_id)
        - Le dictionnaire matchant word a word_id
        - Le dictonnaire matchant doc a doc_id
        """
        j=0
        k=0
        content_parsed = []
        dic_docs={}
        dic_termes={}
        for i in range (0,self.nbr_of_folders):
            for file_name in os.listdir('data/cs276/'+str(i)):
                with open('data/cs276/'+str(i)+'/'+file_name,'r') as f:
                    doc_id = j
                    dic_docs[file_name]=doc_id
                    j=j+1
                    content = f.read()
                    words = word_tokenize(content)
                    for w in words:
                        if w not in dic_termes:
                            w_id = k
                            dic_termes[w]=w_id
                            k=k+1
                        content_parsed.append((w_id,doc_id))
        return content_parsed,dic_docs,dic_termes


    def map(self,partition):
        """
        Fonction map qui ajoute a un dictionnaire dont les clefs sont les mots des elements du type (Doc_id,1)

        """
        map_index={}
        for word in partition:
            if word[0] not in map_index:
                map_index[word[0]]=[]
            map_index[word[0]].append((word[1],1))
        return map_index


    def reduce(self,partition,index_inv_final):
        """
        La fonction reduce renvoie un dictionnaire dont les clefs sont les mots.
        Les valeurs sont elles memes des dictonnaires dont les clefs sont les doc_id et les valeurs le nombre d'apparition
        """
        for word in partition:
            if word not in index_inv_final:
                index_inv_final[word]={}
            for elem in partition[word]:
                doc_id=elem[0]
                cnt = elem[1]
                if doc_id in index_inv_final[word]:
                    index_inv_final[word][doc_id]=index_inv_final[word][doc_id]+cnt
                else:
                    index_inv_final[word][doc_id]=cnt
        return index_inv_final

    def shuffle(self):
        """
        Create three different clusters of tokens
        """
        partition={}
        partition[1]=[]
        partition[2]=[]
        partition[3]=[]
        for w in self.tokens:
            if w[0]%3==0:
                partition[1].append(w)
            elif w[0]%3==1:
                partition[2].append(w)
            elif w[0]%3==2:
                partition[3].append(w)
        return partition

    def map_reduce_index(self):
        """
        On commence par regrouper les tokens dans les clusters suivants par ordre alphabetique:
        """
        index_inv={}
        partition=self.shuffle()
        # On applique la fonction map sur chacun des clusters
        for part in partition:
            index_inv[part]=self.map(partition[part])
        # On applique la fonction reduce aux clusters et on fait grossir notre index inverse finale
        index_inv_final={}
        for part in index_inv:
            index_inv_final=self.reduce(index_inv[part],index_inv_final)
        return index_inv_final
