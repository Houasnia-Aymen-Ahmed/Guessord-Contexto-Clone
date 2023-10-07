import os,sys
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..' ,'backend'))
sys.path.append(backend_dir)
django.setup()

from api.models import Game
from api.similarity_checker.load_glove_vectors import load_glove_vectors

def get_random_word_from_glove():
    
    glove_vectors=load_glove_vectors()
    if glove_vectors is None:
        load_glove_vectors()

    valid_words = [word for word in glove_vectors.keys() if word.isalpha()]

    if not valid_words:
        return None

    random_word = random.choice(valid_words)
    return random_word

random_word = get_random_word_from_glove()
game = Game(secret_word=random_word)
game.save()

