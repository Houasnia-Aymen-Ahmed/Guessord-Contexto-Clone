from django.db import models

# Create your models here.
class Words (models.Model):
  word = models.CharField(max_length=50)
  def __str__(self):
      return self.word


class Game(models.Model):
    secret_word = models.CharField(max_length=50)

    def __str__(self):
        return f'Game: {self.secret_word}'

class GuessedWord(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user_word = models.CharField(max_length=50)
    similarity_score = models.FloatField()

    def __str__(self):
        return f'Guessed Word: {self.user_word} (Score: {self.similarity_score})'
      