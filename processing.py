import pandas as pd
from gensim.models import KeyedVectors
import numpy as np
from gensim.corpora import Dictionary
from keras.preprocessing import sequence
import pickle as pkl


#declare global variables
vector_size = 300
vocab_size = 3000
seq_length = 10
word_vectors = None

Start_vector = np.zeros(vector_size,)
Unk_vector = np.random.randn(vector_size,)
Padding_vector = np.random.randn(vector_size,)
keep_n = vocab_size #Size of dictionary


def load_word_vectors(File = 'GoogleNews-vectors-negative300.bin.gz'):
    word_vectors = KeyedVectors.load_word2vec_format(File, binary=True)
    return word_vectors



#function to split text data, drop punctuation
def splitting(text):
    words = text.split()
    table = str.maketrans('', '', ".,'")
    words = [w.translate(table) for w in words]
    return words

def padding(sequence, seq_length):
    while len(sequence) < seq_length:
        sequence.append("<PAD>")
    while len(sequence) > seq_length:
        sequence = sequence[:-1]
    return sequence

#function to map the list of words to vectors
def map_words_to_vectors (text): #takes a list of words
    list_of_vectors = [] #the list of vectors to be returned
    for word in text:
        try:
            if word == "</s>":
                list_of_vectors.append(Start_vector) #append the Start Vector
            elif word == "<PAD>":
                list_of_vectors.append(Padding_vector) #append the Padding Vector
            else:
                list_of_vectors.append(word_vectors[word]) #append the word vector
        except: #except if the word is not included in the Google Corpus
            list_of_vectors.append(Unk_vector)
    return list_of_vectors

#function to one hot the sentence
def one_hot(sentence):
    one_hotted_list = []
    for number in sentence:
        array = np.zeros(keep_n+2) #add two .. 1) </s> 3000 2)padding 3001
        array[number] = 1
        one_hotted_list.append(array)
    return one_hotted_list

#indexes the word ie maps a word to a number
def indexing(Corpus,keep_n,length,samples): #samples => number of samples in the corpus to take
    sentences = [] #list of list of words
    for i in range(len(Corpus)):
        sentences.append(Corpus['Output'][i]) #puts all the lists of words(Output[i]) into the "sentences" list
    dct = Dictionary(sentences)
    dct.filter_extremes(keep_n) #keeps the top n words
    dictionary = (dct.token2id) #dictionary now has all the words mapped to a number
    #newsentences will be a list of lists that only includes the top n indexes
    newsentences = []
    for sentence in sentences: #for each list in the sentences list
        newsentence = [keep_n] #pad the sentence with the </s> token
        for item in sentence: #for each word in the sentence
            if (item in dictionary): #check if the word is top n frequent word
                newsentence.append(dictionary[item]) #append
            else:
                pass #otherwise do nothing
        newsentences.append(newsentence) #append the sentence after each word has been iterated through
    #all the sentences in X_train are of length 10, ie if longer - truncate, if shorter - pad
    X_train = sequence.pad_sequences(newsentences, maxlen=length, value=3001, padding="post", truncating="post")
    temp = []
    for i in range(samples):
        temp.append(one_hot(X_train[i]))
    return temp

#collect all the lists into one list
def collect(df,column,length):
    output = []
    for i in range(length):
        output.append(df[column][i])
    output = np.array(output)
    return output


#Format and Map string to word vector
def split_and_pad(String):
    String_list = splitting(String)
    String_list = padding(String_list, seq_length)
    # Vectors = map_words_to_vectors(String_list)
    return String_list


def train_prep_default():
    Corpus = pd.read_csv(r"corpus.csv",encoding = "ISO-8859-1")
    Corpus['Input'] = Corpus['Input'].astype(str).apply(split_and_pad)
    Corpus['Output'] = Corpus['Output'].astype(str).apply(split_and_pad)
    Corpus['Input_Vectors'] = Corpus['Input'].apply(map_words_to_vectors)
    Corpus['Output_Vectors'] = Corpus['Output'].apply(map_words_to_vectors)
    one_hot_vectors = np.array(indexing(Corpus,keep_n,seq_length,vocab_size))
    Output = collect(Corpus,"Output_Vectors",vocab_size)
    Input = collect(Corpus,"Input_Vectors",vocab_size)
    
    return one_hot_vectors,Output,Input    


def test_run ():
    #Corpus = pd.read_csv(r"corpus.csv",encoding = "ISO-8859-1")
    global word_vectors
    word_vectors = load_word_vectors()
    while True:
        test = str(input("put some stuff here: "))
        print(string_to_vec(test))

    



