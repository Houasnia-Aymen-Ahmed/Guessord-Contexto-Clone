from rest_framework import serializers
from .models import *

class WordsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Words
    fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GuessedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuessedWord
        fields = '__all__'

