from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=100,null=True)
    total_questions = models.IntegerField(null=True)
    # questions = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='questions',null=True)
    created_At = models.DateTimeField(auto_now_add=True,null=True)
    updated_At = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        db_table = 'quiz'
        
class Question(models.Model):
    question = models.CharField(max_length = 250,null=True)
    questionOptions = ArrayField(models.CharField(max_length = 100,blank=True,null=True))
    answer = models.CharField(max_length=100,null=True)
    type = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name = 'quiz_id',null=True)
    created_At = models.DateTimeField(auto_now_add=True,null=True)
    updated_At = models.DateTimeField(auto_now_add=True,null=True)
    
    
    class Meta:
        db_table = 'question'
        
class UserAnswers(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question_id')
    profile = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_id')
    answer = models.CharField(null=False,max_length=100)
    


    
    # user_answer = UserAnswers.filter(user,questtion).values_list('answer',flat=True)
    # question = Question.filter(question,answer__in=user_answer).count()
    
    
    


# class Options(models.Model):
#     Option1 = models.CharField(max_length = 100)
#     Option2 = models.CharField(max_length = 100)        
#     Option3 = models.CharField(max_length = 100)        
#     Option4 = models.CharField(max_length = 100)        
            
# class Question(models.Model):
#     question = models.CharField(max_length = 250)
#     options = models.ManyToManyField(Options)
#     answer = models.CharField(max_length=100)
    
# class Quiz(models.Model): 
#     quizName = models.CharField(max_length = 250)
#     total_questions = models.IntegerField()
#     question = models.ForeignKey(Question,on_delete=models.CASCADE)
    
    
    
