from rest_framework import serializers
from .models import Profile



class CreateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=250,required=False)
    email = serializers.EmailField(required = False)
    phone_number = serializers.CharField(max_length=30,required=False)
    
    
    

# class UserSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Profile
    #     fields = '__all__'