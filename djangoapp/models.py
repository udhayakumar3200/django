from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    username = models.CharField(max_length=30,null=True,unique=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=30,null=True,blank=True)
    

