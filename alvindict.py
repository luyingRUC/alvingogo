def getKeyByValue(targetValue,targetDict, mode):
    # This function returns the first key whose values match with the targetValue
    # Parameter: 
        # targetValue: the target value we want to match with
        # dict: the dictionary you want to search from
        # mode: the data type of value for that key
            # 'string': matched when targetValue = value(string)
            # 'list': matched wehn target in value(list)
            # 'dict': matched when target is one of the keys in value(dictionary) 
    if(mode == "string"):
        for _key in targetDict.keys():
            if(targetValue == targetDict[key]):
                return _key
        return None
    elif(mode == "list"):
        for _key in targetDict.keys():
            if(targetValue in targetDict[_key]):
                return _key
        return None
    elif(mode == "dict"):
        for _key in targetDict.keys():
            if(targetValue in targetDict[_key].keys()):
                return _key    
        return None
    else: 
        print("Parameter `mode` is illegal")
        return None