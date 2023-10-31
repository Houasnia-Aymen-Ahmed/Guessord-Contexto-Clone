from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .similarity_checker.get_similarity_rank import get_similarity_rank
#from .utils.word_generator import get_random_word_from_glove
from .models import *
from .serializers import *

# Create your views here.

class WordView(generics.RetrieveAPIView):
  queryset = Words.objects.all()

  def get (self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = WordsSerializer(queryset, many=True)
    print(serializer.data)
    return Response(serializer.data)
  
class GameListView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GuessedWordListView(generics.ListCreateAPIView):
    queryset = GuessedWord.objects.all()
    serializer_class = GuessedWordSerializer

class GuessWordView(APIView):
    def post(self, request, *args, **kwargs):
        user_word = request.data.get('guess').lower()
        game_id = request.data.get('game_id')
        game = Game.objects.get(id=game_id)
        secret_word = game.secret_word.lower()

        """ similarity = get_similarity_rank_annoy(secret_word,user_word) """
        rank = get_similarity_rank(secret_word,user_word)
        
        if rank is not None and rank >= 0 :
            guessed_word = GuessedWord.objects.create(
                game=game,
                user_word=user_word,
                similarity_score=rank
            )
            return Response({
                'similarity_score': rank,
                'guessed_word': guessed_word.user_word
            }, status=status.HTTP_200_OK)
        else:
            error_message = f'Sorry the words "{user_word}" is not in the vocabulary. Please try another word'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)