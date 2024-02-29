from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=100,null=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,null=True, related_name='questions')
    text = models.CharField(max_length=250,null=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True, related_name='answers')
    text = models.CharField(max_length=100,null=True)
    is_correct = models.BooleanField(default=False)

class UserAnswers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,null=True,related_name='user_answers')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True)
    is_correct = models.BooleanField(default=False)
    
    
    
    
    
    