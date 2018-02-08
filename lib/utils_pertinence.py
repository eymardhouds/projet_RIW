from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import matplotlib.pylab as plt

def parser_queries_results(queries):
    with open('data/CACM/qrels.text','r') as doc:
        content = doc.readlines()
        content = [x.strip() for x in content]
        q_res={}
        for line in content:
            line = line.split()
            if int(line[0]) not in q_res:
                q_res[int(line[0])]=[]
            q_res[int(line[0])].append(int(line[1]))
            for i in queries.keys():
                # We have to add this condition because some values are missing in the document we try to parse
                if i not in q_res.keys():
                    q_res[i]=[]
    return q_res

def parser_queries_text(commonwords):
    with open('data/CACM/query.text','r') as doc:
        content = doc.readlines()
        content = [x.strip() for x in content]
        current_id=0
        queries={}
        i=0
        tokenizer = RegexpTokenizer(r'\w+')
        while i<len(content):
            line = content[i]
            if line[:2]==".I" and i<len(content):
                current_id=int(line[2:])
                i=i+2
                line = content[i]
                while line[:2]!='.N' and i<len(content):
                    if current_id not in queries:
                        queries[current_id]=[]
                    for t in tokenizer.tokenize(line):
                        queries[current_id].append(t)
                    queries[current_id]=[r.lower() for r in queries[current_id]]
                    for w in queries[current_id]:
                        if w in commonwords or w in stopwords.words('english'):
                            queries[current_id].remove(w)
                    i=i+1
                    line = content[i]
            i=i+1
    return queries

def get_commonwords():
    with open('data/CACM/common_words','r') as doc:
        content = doc.readlines()
    common_words = [x.strip() for x in content]
    return common_words


def get_rappel_and_precision(results,q_res,dic_docs):
    rappel={}
    precision={}
    #Initialisation
    for i in q_res:
        rappel[i]={}
        precision[i]={}
        for j in range(1,len(dic_docs)+1):
            rappel[i][j]=0
            precision[i][j]=0

    for q in q_res:
        results[q]=[m[0] for m in results[q]]
        # gestion du seuil
        for seuil in range(1,len(dic_docs)+1):
            results_tmp=results[q][:seuil]
            for elem_found in results_tmp:
                if elem_found in q_res[q]:
                    rappel[q][seuil]=rappel[q][seuil]+1
            for elem_pertin in q_res[q]:
                if elem_pertin in results_tmp:
                    precision[q][seuil]=precision[q][seuil]+1

            # Normalisation
            if len(q_res[q])!=0:
                rappel[q][seuil]=float(rappel[q][seuil])/float(len(q_res[q]))
            else:
                rappel[q][seuil]=0
            precision[q][seuil]=float(precision[q][seuil])/float(seuil)
            if precision[q][seuil]>1 or rappel[q][seuil]>1:
                print(precision[q][seuil])
                print(rappel[q][seuil])

    return precision,rappel

def get_f_e_measures(precision,rappel,dic_docs,q_res):
    e_measures={}
    f_measures={}
    for i in q_res:
        e_measures[i]={}
        f_measures[i]={}
        for j in range(1,len(dic_docs)+1):
            e_measures[i][j]=0
            f_measures[i][j]=0
    for q in q_res:
        for seuil in range(1,len(dic_docs)+1):
            if precision[q][seuil]!=0 or rappel[q][seuil]!=0:
                e_measures[q][seuil] = 1 - 2 * (precision[q][seuil] * rappel[q][seuil] / (precision[q][seuil] + rappel[q][seuil]))
                f_measures[q][seuil] = 2 * (precision[q][seuil] * rappel[q][seuil] / (precision[q][seuil] + rappel[q][seuil]))
            else:
                e_measures[q][seuil]=0
                f_measures[q][seuil]=0
    return e_measures,f_measures

def plot_precision_rappel(precision,rappel,dic_docs,q_res):
    avg_precision={}
    avg_rappel={}
    len_q=len(q_res)
    for i in range(1,len(dic_docs)+1):
        avg_precision[i]=0
        avg_rappel[i]=0
    for seuil in range(1,len(dic_docs)+1):
        for q in q_res:
            avg_precision[seuil] = precision[q][seuil]+avg_precision[seuil]
            avg_rappel[seuil]= rappel[q][seuil]+avg_rappel[seuil]
        avg_precision[seuil]=avg_precision[seuil]/len_q
        avg_rappel[seuil]=avg_rappel[seuil]/len_q
    plt.figure()
    plt.title('Precision and recall')
    plt.plot(avg_precision.values(), avg_rappel.values())
    plt.show()
    return avg_precision,avg_rappel
