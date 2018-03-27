import string
import numpy as np
# from nltk.corpus import brown
from gensim.models import KeyedVectors
import tensorflow as tf
#switches the key value pairs in a dictionary
sess = tf.Session()
def switch_key_value (dictionary):
    with sess.as_default():
        dictionary = {tuple(y.eval()): x for x, y in dictionary.items()}
    return dictionary

#character level
def string_to_character_embeddings(filename):
        file = open(filename, 'r')
        raw_text = file.read()
        file.close()
        words = raw_text.split()
        tokens = ' '.join(words)
        punctuation_table = str.maketrans('', '', string.punctuation)
        punctuation_stripped = [token.translate(punctuation_table) for token in tokens]
        number_table = str.maketrans('', '', string.digits)
        number_stripped = [token.translate(number_table) for token in tokens]
        lowercased = [token.lower() for token in tokens]
        chars = sorted(list(set(lowercased)))
        mapping = dict((c, i) for i, c in enumerate(chars))

        size = len(mapping)
        for i in range(size):
            zeros = np.zeros(size)
            zeros[i] = 1
            one_hot_vector = zeros #[np.newaxis].T  uncomment if the shape is (n,1)
            key = list(mapping.keys())[i]
            mapping[key] = tf.convert_to_tensor(one_hot_vector)
        return mapping
#
# string_to_charcater_dictionary = string_to_character_embeddings("test.txt")
# character_to_string_dictionary = switch_key_value(string_to_charcater_dictionary)
# print(character_to_string_dictionary)
#
# corpus is a list of strings
word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

def word_embeddings_mapping(corpus):
    mapping = dict((c, i) for i, c in enumerate(corpus)) #initilize the values to something
    size = len(mapping)
    for i in range(size):
        word = list(mapping.keys())[i]
        word_embedding = word_vectors[word] #obtain mapping
        key = list(mapping.keys())[i]
        mapping[key] = word_embedding
    return mapping





# corpus = brown.words(categories='hobbies')[0:3]
print(word_embeddings_mapping(['animal']))


