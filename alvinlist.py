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
