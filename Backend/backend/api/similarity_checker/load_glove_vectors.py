import os
import pickle
import time
from scipy import spatial
import numpy as np
from annoy import AnnoyIndex
from sklearn.neighbors import BallTree

current_dir = os.path.dirname(os.path.abspath(__file__))
model_dimension = "50"
glove_path = os.path.join(current_dir, f"glove/glove.6B.{model_dimension}d.txt")
index_annoy_path = os.path.join(current_dir, "annoy_index.ann")

def load_glove_vectors():
    global glove_vectors
    vectors_path = os.path.join(current_dir, f"glove_vectors_{model_dimension}d.pkl")

    if os.path.exists(vectors_path):
        with open(vectors_path, "rb") as f:
            glove_vectors = pickle.load(f)
    else:
        glove_vectors = {}

        with open(os.path.join(glove_path), "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], dtype="float32")
                glove_vectors[word] = vector

        with open(vectors_path, "wb") as f:
            pickle.dump(glove_vectors, f)
    return glove_vectors


glove_vectors = load_glove_vectors()


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
    if similarity is not None:
        print(
            f'(true)The cosine similaritys between "{secret_word}" and "{user_input}" is {similarity}.'
        )
    else:
        print(
            f'(false)One or both of the words "{secret_word}" and "{user_input}" are not in the GloVe vocabulary.'
        )
    return similarity


def get_similarity_rank(word, user_input):
    if glove_vectors is None or word not in glove_vectors:
        return None
    target_vector = glove_vectors[word]
    similarity_table = {
        w: 1 - spatial.distance.cosine(target_vector, vec)
        for w, vec in glove_vectors.items()
        if w != word
    }

    sorted_similarity = sorted(similarity_table.items(), key=lambda x: x[1], reverse=True)
    return next(
        i for i, (w, _) in enumerate(sorted_similarity, 1) if w == user_input
    )

def build_annoy_index():
    target_dimension = int(model_dimension)
    index = AnnoyIndex(target_dimension, 'euclidean')
    for i, (_, vec) in enumerate(glove_vectors.items()):
        index.add_item(i, vec)
    index.build(50)
    index.save(index_annoy_path)
    return index

def load_annoy_index():
    target_dimension = int(model_dimension)
    index = AnnoyIndex(target_dimension, 'euclidean')
    index.load(index_annoy_path)
    return index

def get_similarity_rank_annoy(word, user_input):
    start_time = time.time()
    index = load_annoy_index()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds") 
    if glove_vectors is not None and word in glove_vectors:
        target_index = list(glove_vectors.keys()).index(word)
        similar_indices = index.get_nns_by_item(target_index, len(glove_vectors))
        return similar_indices.index(list(glove_vectors.keys()).index(user_input)) + 1
    else:
        return None
