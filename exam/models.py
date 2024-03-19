from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100,null=True)
    
    class Meta:
        db_table = "Category"
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory_name = models.CharField(max_length=100,null=True)
    
    class Meta:
        db_table = "SubCategory"
    
class Exam(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True)
    exam_name = models.CharField(max_length=100,null=True)
    duration = models.DurationField(null=True)
    
    class Meta:
        db_table = "Exam"
    
class Ques(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True)
    question = models.CharField(max_length=200)
    answers = ArrayField(models.JSONField(null=False,blank=False,default=dict),null=True)
    correct_option = models.JSONField(null=False,blank=False,default = dict)
    
    class Meta:
        db_table = "Ques"

class CandidateAnswer(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(Ques,on_delete=models.CASCADE,null=True)
    answer = models.JSONField(null=True,blank=True,default=dict)
    is_correct = models.BooleanField(default=None,null=True)
    
    class Meta:
        db_table = "CandidateAnswers"

class Scores(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True)
    score = models.FloatField(null=False,default = 0.0)
    
    class Meta:
        db_table = "Scores"
     
    
    
    