from django.urls import path
from .views import *

urlpatterns = [
    path('games/', GameListView.as_view(), name='game-list'),
    path('guessed-words/', GuessedWordListView.as_view(), name='guessed-word-list'),
    path('guessed-word/', GuessWordView.as_view(), name='guessed-word'),
]