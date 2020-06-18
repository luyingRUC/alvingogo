import os
import pickle
import random
import logging
import numpy as np

from gensim.models import word2vec

def createWord2vecs(path_corpus, path_word2vec_pkl):
    #该函数生成word2vec_1.pkl文件，作为RNN 的输入
    logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
    sentences = word2vec.Text8Corpus(path_corpus)
    model = word2vec.Word2Vec(sentences, size=50)
    print(model.wv)
    print(type(model.wv))
    model.save(path_word2vec_pkl)

def getVector(pth_pkl, keyword):
    # This function get a specific vector from the pre-trained word2vec model
    key = ""  
    with open(pth_pkl, "rb") as f:
        flag =0
        word_vec = pickle.load(f)
        for (key,value) in word_vec.items():
            if key == keyword :
                flag = 1
                return key , value
        if flag==0:
            return "nothing"


def gene_corpus_from_jobcsv(csvpth, corpuspth):
    # define a function which: 
    #   1. extract all skills from skill collumn in a .csv file 
    #   2. for skills with more than one word, connect each word with "-"
    #   3. generate a corpus with all news skills suquently ordered as they are in the original sentense
    csvdf = pd.read_csv(csvpth, delimiter=',')
    csvdf = csvdf[csvdf['skl_dirctmatch'].notnull()]
    skill_dict = {}
    skill_list = []
    for ele in csvdf['skl_dirctmatch']:
        if (ele):
            for skill in ele.split(","):
                # if the skill contains more than one word, combine it
                if(len(skill.split(" "))>1):
                    # change the _ into - to merge all the words in this skill
                    skill = skill.replace(" ", "-")
                    # skill_dict[skill] = skill_dict[skill] + 1
                    skill_list.append(skill)
                # if the skill contains more only one word, save it
                else:
                    # skill_dict[skill] = skill_dict[skill] + 1
                    skill_list.append(skill)
        else: pass  

    if (len(skill_list)):
        with open(corpuspth,"w") as corpusfile: 
            for skill in skill_list: 
                corpusfile.write(skill + " ")
            print("corpus generated at %s" %(corpuspth))
    else:
        print("there is no skills generated...")
    return corpuspth




def load_pkl(pth_pkl):
    with open(pth_pkl, "rb") as f:
        word_vec = pickle.load(f)
        max_number_printline = 3
        
        current_number_println = 0
        for (key,value) in word_vec.items():
            
            
            current_number_println += 1
            if current_number_println < max_number_printline:
                print(key, value)
                print("the types of key and values are : ",type(key),"  ", type(value))
                print("the len of value is : ", len(value))
            else:
                break
        print("finish load_pkl(), there are totally %d terms in pkl file" %(current_number_println))
  
def print_pkl(pth_pkl, keyword):
    with open(pth_pkl, "rb") as f:
        word_vec = pickle.load(f)
        flag = 0
        print("=======", word_vec[keyword])
        for (key,value) in word_vec.items():
            if key == keyword:
                print("key =" , key, "value = " , value)
                flag = 1
        print("after searching %s, flag = %d" %(pth_pkl, flag))
          
def create_pkl(data, output_path):
    output = open(output_path, 'wb')
    pickle.dump(data, output)
    output.close()
    
    print("finished writing to .pkl, saved at %s" %(output_path))
    
    return      

def get_single_pkl(pth_pkl, keyword):
    key = ""  
    with open(pth_pkl, "rb") as f:
        flag =0
        word_vec = pickle.load(f)
        for (key,value) in word_vec.items():
            if key == keyword :
                flag = 1
                return key , value
        if flag==0:
            return "nothing"

def insert_pkl(pth_pkl_from, pth_pkl_into, keyword):
    key = ""
    values = []
    word_vec= {}
    if get_single_pkl(pth_pkl_wiki, keyword) != "nothing":
        key, values = get_single_pkl(pth_pkl_wiki, "<UNK>")
        with open(pth_pkl_into,"rb") as f:
            word_vec = pickle.load(f)                  
            #追加写入词典：
            word_vec[key] = values
            f.close()
            
        
        output = open(pth_pkl_into, 'wb')
        pickle.dump(word_vec, output)
        output.close()
        print("写入完成")
            
        if get_single_pkl(pth_pkl_into,keyword) != "nothing":
            print(get_single_pkl(pth_pkl_into,keyword))
            print("inserting succeeded!")
        else:
            print("inserting failed !")
    return  
    

def load_word2vecs(path_wordvec):
    model = word2vec.Word2Vec.load(path_wordvec)    

#    print(model.wv["武汉"])
#    model.wv.get_all_vectors();  # this function get something wrong, I have rewirte it in Gensim.keyedVectors , but it failed to work/..
    
    if len(model.wv.vocab) != 0 :
        return model
    else:
        print("model has no words !")
        return None


def get_wordvec_number(vec_model):
    # This funciton returns the totol number of unique word embeddings in the pre-trained word2vec model 
    n_terms =0
    print("get the total number of KeyedVectors vocabulary ... ")
    for word in vec_model.wv.vocab:
        n_terms = 1+ n_terms
    print("the total number of the vocabulary is %d" %(n_terms))
    return n_terms
    
def get_all_wordvecs(vec_model):
    # This fuction returns a dictionary which contains all ("word", "embedding") pairs, with word name as the key
    dict_wv = {}
    for word in vec_model.wv.vocab:
#        print(word, vec_model.wv.word_vec(word))
        dict_wv[word] = vec_model.wv.word_vec(word).tolist()
    return dict_wv