# Generated by Django 4.2.6 on 2023-10-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_game_guessedword"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="secret_word",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="guessedword",
            name="user_word",
            field=models.CharField(max_length=50),
        ),
    ]
