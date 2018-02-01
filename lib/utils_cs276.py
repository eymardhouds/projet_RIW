# Stanford: Tokens: 25 000 000 et taukke 400 000
import re,math, os, collections,sys,time
from nltk.tokenize import sent_tokenize, word_tokenize

class corpus_cs276:

    def __init__(self):
        self.content_parsed,self.dic_docs,self.dic_termes = self.traitement_corpus() #C'est un grand tableau de tuples (term_id,doc_id)
        self.length_tokens = len(self.tokens)
        self.vocabulary = collections.Counter(x[0] for x in self.token)
        self.length_voc = len(self.vocabulary)
        self.index_inverse = map_reduce_index()

    def traitement_corpus(self):
        """
        Cette fonction renvoie:
        - une liste de tuples (word_id,doc_id)
        - Le dictionnaire matchant word à word_id
        - Le dictonnaire matchant doc à doc_id
        """
        j=0
        k=0
        content_parsed = []
        dic_docs={}
        dic_termes={}
        for i in range (0,10):
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

    def map_reduce_index(self):
        """
        On commence par regrouper les tokens dans les clusters suivants par ordre alphabétique:
        Cluster 1: A-E
        Cluster 2: F-J
        Cluster 3: K-0
        Cluster 4: P-T
        Cluster: W-Z
        """
        cluster_1=["a","b","c","d","e"]
        cluster_2=["f","g","h","i","j"]
        cluster_3=["k","l","m","n","o"]
        cluster_4=["p","q","r","s","t"]
        cluster_5=["u","v","w","x","y","z"]
        # Creation des clusters
        for w in self.token:
            if w[0][0] in cluster_1:
                c = "cluster_1"
            elif w[0][0] in cluster_2:
                c="cluster_2"
            elif w[0][0] in cluster_3:
                c="cluster_3"
            elif w[0][0] in cluster_4:
                c="cluster_4"
            elif w[0][0] in cluster_5:
                c="cluster_5"
            partition[c].append(w)

        # On créé les indexs inversés pour chaque noeud de la partition (Faire 5 threads)
        index_inv={}
        for part in partition:
            for word in partition[part]:
                index_inv[part] ={}
                if word[0] not in index_inv_1:
                    # L'index a la forme: mot_id= (doc_id,counter)
                    index_inv[part][word[0]]=(word[1],1)
                else:
                    #On incrémente le compter si le mot a déjà été vu
                    index_inv[part][word[0]][1]=index_inv[part][word[0]][1]+1


        for elem in index_inv["cluster_1"]:
            if elem in index_inv["cluster_2"]:
                index_inv["cluster2"][elem]=(index_inv["cluster_2"][elem][0],index_inv["cluster_1"][elem][1]+index_inv["cluster_2"][elem][1])
                index_inv["cluster_1"].remove(elem)
        # Et on ajoute à l'index total tout le reste de l'index 2 qui n'est pas déjà dans index_inv_1

        # Làil faut penser à ajouter une opération de fusion !! (genre les mots qui sont dans les deux)
        index_inv["cluster_2"]=index_inv["cluster_2"]+index_inv["cluster_1"]


        for elem in index_inv["cluster_2"]:
            if elem in index_inv["cluster_3"]:
                index_inv["cluster_3"][elem]=(index_inv["cluster_3"][elem][0],index_inv["cluster_2"][elem][1]+index_inv["cluster_3"][elem][1])
                index_inv["cluster_2"].remove(elem)
        index_inv["cluster_3"]=index_inv["cluster_3"]+index_inv["cluster_2"]

        for elem in index_inv["cluster_3"]:
            if elem in index_inv["cluster_4"]:
                index_inv["cluster_4"][elem]=(index_inv["cluster_4"][elem][0],index_inv["cluster_3"][elem][1]+index_inv["cluster_4"][elem][1])
                index_inv["cluster_3"].remove(elem)
        index_inv["cluster_4"]=index_inv["cluster_4"]+index_inv["cluster_3"]

        for elem in index_inv["cluster_4"]:
            if elem in index_inv["cluster_5"]:
                index_inv["cluster_5"][elem]=(index_inv["cluster_5"][elem][0],index_inv["cluster_4"][elem][1]+index_inv["cluster_5"][elem][1])
                index_inv["cluster_4"].remove(elem)
        index_inv["cluster_5"]=index_inv["cluster_5"]+index_inv["cluster_4"]

        index_inv_final = index_inv["cluster_5"]
        return index_inv_final
