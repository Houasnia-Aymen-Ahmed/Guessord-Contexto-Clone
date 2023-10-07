import os
import pickle
from scipy import spatial
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
model_dimension = "50"
glove_path =  os.path.join(current_dir,"glove/glove.6B."+model_dimension+"d.txt")


def load_glove_vectors():
    global glove_vectors
    vectors_path = os.path.join(current_dir, 'glove_vectors_'+model_dimension+'d.pkl')

    if os.path.exists(vectors_path):
        with open(vectors_path, 'rb') as f:
            glove_vectors = pickle.load(f)
    else:
        glove_vectors = {}

        with open(os.path.join(glove_path), 'r', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], dtype='float32')
                glove_vectors[word] = vector

        with open(vectors_path, 'wb') as f:
            pickle.dump(glove_vectors, f)
    return glove_vectors

glove_vectors=load_glove_vectors()

def get_word_vector(word):
    if glove_vectors is not None and word in glove_vectors:
        return glove_vectors[word]
    else:
        return None

def get_similarity(word1, word2):
    vec1 = get_word_vector(word1)
    vec2 = get_word_vector(word2)
    
    if vec1 is not None and vec2 is not None:
        return 1 - spatial.distance.cosine(vec1, vec2)
    else:
        return None

def check_similarity(secret_word, user_input):
    similarity = get_similarity(secret_word, user_input)
    print("in check similarity")
    if similarity is not None:
        print(f'(true)The cosine similaritys between "{secret_word}" and "{user_input}" is {similarity}.')
    else:
        print(f'(false)One or both of the words "{secret_word}" and "{user_input}" are not in the GloVe vocabulary.')
    return similarity
