import nltk
# nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer, regexp_tokenize
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk import pos_tag
from stop_words import get_stop_words
get_stop_words("en").remove("and")

import re




def generateCleanText(intputText, outputType):
    # This function cleans the intput string and return a cleaned string / list of cleaned words
    ''' outputType = 
        1. list: return a list of clean words : like [Apple, has, power, compelling, to, Microsoft]
        2. string: return a string of clean words, each of which is joint by " ", like "Apple has power compelling to Microsoft"
    '''

    # Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', intputText)

    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    text = text.lower()

    # clean and tokenize document string
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    # filter the POS tags, if the token is not a noun or adj, chop it out
    # ok_tags = ['JJ', 'JJR', 'JJS','NN', 'NNS','NNP','NNPS','FW']
    # ok_tags = ['NN', 'NNS','NNP','NNPS','FW', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    # word_tuples = pos_tag(tokens)
    # tokens2 = []
    # for _tuple in word_tuples:
    #     if _tuple[1] in ok_tags:
    #         tokens2.append(_tuple[0])

    # remove stop words from tokens
    # create English stop words list
    en_stop = get_stop_words('en')
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # # stem tokens
    # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # Lemmatization
    lemmalist = []
    lemmatizer = WordNetLemmatizer()
    for word in stopped_tokens:
        lemmalist.append(lemmatizer.lemmatize(word))

    # multiples : take all the single characters out of list
    multiples = []
    for lemma in lemmalist:
        # for single character, take them off:
        if(len(lemma) > 1):
            multiples.append(lemma)

    if(outputType == "list"):
        return multiples
    elif(outputType == "string"):
        multiples = " ".join(multiples)
        return multiples
    else:
        print("the outputType is not valid, please check again ")
        return None


def getLastWordStemmed(string, outputType):
    # This function only stem the last word of the input phrase

    # Create p_stemmer of class PorterStemmer
    text = string.lower()

    # clean and tokenize document string
    tokens = regexp_tokenize(string, r'\S+')
    # tokens = tokenizer.tokenize(text)

    # remove stop words from tokens
    # create English stop words list
    en_stop = get_stop_words('en')
    stopped_tokens = [i for i in tokens if not i in en_stop]

    
    # Only stemmilize the last word when it is formatted only by alpha characters
    p_stemmer = PorterStemmer()
    stemmed_tokens = []
    if (len(stopped_tokens) >0):
        for i in range(0,len(stopped_tokens)):
            if (i == len(stopped_tokens)-1):
                if(stopped_tokens[i].isalpha()):
                    stopped_tokens[i] = p_stemmer.stem(stopped_tokens[i])

    # multiples : take all the single characters out of list
    multiples = []
    for word in stemmed_tokens:
        # for single character, take them off:
        if(len(word) > 1):
            multiples.append(word.strip())


    if(outputType == "list"):
        return multiples
    elif(outputType == "string"):
        multiples = " ".join(multiples)
        return multiples
    else:
        print("the outputType is not valid, please check again ")
        return None


def getLemmed(string, outputType):
    # This function lemmilize all the words in a phrase/sentence 

    # Create p_stemmer of class PorterStemmer
    text = string.lower().strip()

    # Remove punctuations
    # text = re.sub('[^a-zA-Z]', '', text)

    # # remove tags
    # text = re.sub("&lt;/?.*?&gt;", "", text)

    # clean and tokenize document string
    tokens = regexp_tokenize(text, r'\S+')
    # tokens = tokenizer.tokenize(text)

    # remove stop words from tokens
    # create English stop words list
    en_stop = get_stop_words('en')
    stopped_tokens = [i for i in tokens if not i in en_stop]    

    # Lemmatization
    lemmalist = []
    lemmatizer = WordNetLemmatizer()
    for word in stopped_tokens:
        if(word.isalpha()):
            lemmalist.append(lemmatizer.lemmatize(word))
        else:
            lemmalist.append(word)

    # multiples : take all the single characters out of list
    multiples = []
    for lemma in lemmalist:
        # for single character, take them off:
        if(len(lemma) > 1):
            multiples.append(lemma)

    if(outputType == "list"):
        return multiples
    elif(outputType == "string"):
        multiples = " ".join(multiples)
        return multiples
    else: 
        print("the output type is invalid, please try again")
        return None


def getAllLemmedLastStemmed(string, outputType):
    # This function lemmlizes all but the last word of the input phrase, and stemmilizes the last word

    # clean and tokenize document string
    tokens = regexp_tokenize(string, r'\S+')
    # tokens = tokenizer.tokenize(text)

    # remove stop words from tokens
    # create English stop words list
    en_stop = get_stop_words('en')
    stopped_tokens = [i for i in tokens if not i in en_stop]    

    # Lemmatization: lem each word that only contains alpha characters
    lemmalist = []
    lemmatizer = WordNetLemmatizer()
    for word in stopped_tokens:
        if(word.isalpha()):
            lemmalist.append(lemmatizer.lemmatize(word))
        else:
            lemmalist.append(word)

    # stem the last word if it contains only alpha characters
    stemmed_tokens = []
    p_stemmer = PorterStemmer()
    for i in range(len(lemmalist)):
        if (i == len(stopped_tokens) -1):
            word = lemmalist[i]
            if(word.isalpha()):
                stemmed_tokens.append(p_stemmer.stem(word))
            else: 
                stemmed_tokens.append(word)       
        else:
            stemmed_tokens.append(lemmalist[i])
    
    # multiples : take all the single characters out of list
    multiples = []
    for word in stemmed_tokens:
        # for single character, take them off:
        if(len(word) > 1):
            multiples.append(word.strip())

    if(outputType == "list"):
        return multiples
    elif(outputType == "string"):
        multiples = " ".join(multiples)
        return multiples
    else: 
        print("the output type is invalid, please try again")
        return None
