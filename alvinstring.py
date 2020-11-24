from pattern.text.en import singularize


#  定义统计字符串的方法
def calcu_sub_str_num(mom_str, sun_str):
    # calculate how many times a substring appears in a mother string

    #   print('打印母字符串：',mom_str)   #打印出母字符串
    #   print( '打印子字符串：',sun_str)  #打印出子字符串
    #   print('打印母字符串长度：',len(mom_str)) #打印出母字符串长度
    #   print( '打印子字符串长度：',len(sun_str))  #打印出子字符串长度
    count = 0  # 定义计数器初始值
    # 使用循环遍历字符串，第一次循环，通过切片获取下标从0开始与子字符串长度一致的字符串，并与字符串比较，如果等于子字符串count+1
    # 第二次循环，通过切片获取下标从1开始与子字符串长度一致的字符串，并与字符串比较，如果等于子字符串则count+1，以此类推直到遍历完成
    for i in range(len(mom_str)-1):  # 因为i的下标从0开始，所以len（mom_str）-1
        if mom_str[i:i+len(sun_str)] == sun_str:
            count += 1
    return count



def getText(inputstring):
    # This function transfer a inputstring to "" if it is "None"
    # Because select results from mysql, there are always results like "None" when the target column is empty

    if (inputstring == None): 
        return ""
    else:
        return inputstring


def getLem(_word, _type):
    # to get the original format of a word, say: drugs --> drug
        # should specialize word tags, like "noun", "verb"
    lemmatizer = ns.WordNetLemmatizer()
    _word = _word.strip().lower()
    result = lemmatizer.lemmatize(_word,_type)
    
    return result


def get_lcase_singular(inputstring):

    result = singularize(inputstring.strip().lower())

    return result


def get_lcase(inputstring):

    result = inputstring.strip().lower()

    return result