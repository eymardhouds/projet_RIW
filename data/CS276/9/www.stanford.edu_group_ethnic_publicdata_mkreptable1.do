do file to produce table 1 results from replication data set use repdata clear model 1 logit onset warl gdpenl lpopl lmtnest ncontig oil nwstate instab polity2l ethfrac relfrac nolog model 2 logit ethonset warl gdpenl lpopl lmtnest ncontig oil nwstate instab polity2l ethfrac relfrac if second 049999 nolog model 3 logit onset warl gdpenl lpopl lmtnest ncontig oil nwstate instab anocl deml ethfrac relfrac nolog model 4 logit emponset empwarl empgdpenl emplpopl emplmtnest empncontig oil nwstate instab empethfrac nolog model 5 logit cowonset cowwarl gdpenl lpopl lmtnest ncontig oil nwstate instab anocl deml ethfrac relfrac nolog