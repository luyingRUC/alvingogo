def listDeduplicate(inputList):
    # this function helps to deduplicate elements in the given input list
    return list(dict.fromkeys(inputList))

def getMeanList(inputList):
    return sum(inputList) / len(inputList)