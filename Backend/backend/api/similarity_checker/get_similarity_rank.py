import pickle
import gensim.downloader as api
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, f"model.pkl")
with open(model_path, "rb") as f:
      model = pickle.load(f)

def get_similarity_rank(secret_word, user_word,model=model):
    try:
        similar_words = model.most_similar(secret_word, topn=100000)
        low = 0
        high = len(similar_words) - 1
        rank = -1

        while low <= high:
            mid = (low + high) // 2
            if similar_words[mid][0] == user_word:
                rank = mid + 1
                break
            elif similar_words[mid][1] < model.similarity(secret_word, user_word):
                high = mid - 1
            else:
                low = mid + 1
    except KeyError:
        rank = -1

    return rank

""" rank = get_similarity_rank("leather", "fabric")

if rank != -1:
    print(f"The rank is {rank}")
else:
    print("Error: User word not found in similar words.") """