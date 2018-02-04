
def request_parsing(query):
    """
    A|B&C&-D <=> (A OR B) AND C AND not D
    """
    query_parsed=[]
    query = query.split('&')
    for elem_AND in query:
        elem_OR = elem_AND.split('|')
        query_parsed.append(elem_OR)
    return query_parsed


def moteur_bool(query,dic_termes,dic_docs,index_inv):
    """
    INPUTS: terms ids, doc ids, inversed index, end a query
    Return results_postings a list of doc_id respecting the query
    """
    query_parsed=request_parsing(query)
    results_postings = {}
    k=0
    for elem_AND in query_parsed:
        results_postings[k]=[]
        for elem_OR in elem_AND:
            word=elem_OR
            if word in dic_termes and dic_termes[word] in index_inv:
                results_postings[k].append(index_inv[dic_termes[word]])
            else:
                print(elem_OR + " is not in the inversed index")
            if elem_OR[0]=="-":
                # if we have a negation we take all documents id without this word
                not_word = [x for x in range(dic_doc) if x not in index_inv[dic_termes[word]]]
                results_postings[k].append(not_word)

        k=k+1

    # Combine results
    results_merged_OR={}
    t=0
    for res_key in results_postings:
        list_AND = results_postings[res_key]
        t=t+1
        results_merged_OR[t]=[]
        for list_OR in list_AND:
            for elem in list_OR:
                if elem not in results_merged_OR:
                    results_merged_OR[t].append(elem)

    # We only keep the intersection of the elements of results_merged_OR

    results_merged=results_merged_OR[1]
    for res_key in results_merged_OR:
        tab = results_merged_OR[res_key]
        el=0
        while el <len(results_merged):
            elem=results_merged[el]
            if elem not in tab:
                results_merged.remove(elem)
                el=el-1
            el=el+1

    results_cleaned=[]
    for t in results_merged:
        if t not in results_cleaned:
            results_cleaned.append(t)
    return results_cleaned
