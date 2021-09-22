def listDeduplicate(inputList):
    # this function helps to deduplicate elements in the given input list
    return list(dict.fromkeys(inputList))

from numpy import isnan, isinf
def getMeanList(inputList):
    list1 = []
    for l in inputList: 
        if((not isnan(l)) and (not isinf(l)) ):list1.append(l)
    if( len(list1) ==0 ):
        return 1.0
    else: 
        return float(sum(list1) / len(list1))


def unionList(lst1, lst2):
    # get U() of two list
    final_list = list(set(lst1) | set(lst2))
    return final_list