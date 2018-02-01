
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
    #print(index_inv)
    query_parsed=request_parsing(query)
    results_postings = {}
    k=0
    for elem_AND in query_parsed:
        results_postings[k]=[]
        for elem_OR in elem_AND:
            word=elem_OR
            if dic_termes[word] in index_inv:
                results_postings[k].append(index_inv[dic_termes[word]])
            else:
                print(elem_OR + " is not in the inversed index")
            if elem_OR[0]=="-":
                # if we have a negation we take all documents id without this word
                not_word = [x for x in range(dic_doc) if x not in index_inv[dic_termes[word]]]
                print(not_word)
                results_postings[k].append(not_word)

        k=k+1
    # Combine results
    results_merged=results_postings[0][0]

    for res_key in results_postings:
        list_AND = results_postings[res_key]
        print(list_AND)
        for list_OR in list_AND:
            print(list_OR)
            for elem in results_merged:
                if elem not in list_OR:
                    results_merged.remove(elem)

    return results_merged
