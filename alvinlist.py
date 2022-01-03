def listDeduplicate(inputList):
    # this function helps to deduplicate elements in the given input list
    return list(dict.fromkeys(inputList))

from numpy import isnan, isinf

from statistics import mean

def getMeanList(inputList):
    list1 = []
    for l in inputList: 
        if((not isnan(l)) and (not isinf(l)) ):list1.append(l)
    if( len(list1) ==0 ):
        return 1.0
    else: 
        return float(sum(list1) / len(list1))

def getListMeanWithNone(inputlist):
    mean_val = mean([d for d in inputlist if d is not None])
    return mean_val

def getUnion(lst1, lst2):
    # get U() of two list
    final_list = list(set(lst1) | set(lst2))
    return final_list

def getIntersection(list1, list2):
    final_list = list(set(list1) & set(list2))
    return final_list
