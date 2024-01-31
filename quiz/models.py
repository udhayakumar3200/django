from django.db import models

class Quiz(models.Model):
    quizName = models.CharField(max_length = 250)
    total_questions = models.IntegerField()
    