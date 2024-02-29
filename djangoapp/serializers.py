from rest_framework import serializers
from .models import Profile


class CreateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=250, required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=30, required=False)
    
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'    
        
class updateProfileSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Profile
        fields = [
            'username','name','email','phone_number'
        ]
    
    # username = serializers.CharField(max_length=30,required=False,allow_null = True)
    # name = serializers.CharField(max_length=250,required=False)
    # email = serializers.EmailField()
    # phone_number = serializers.CharField(max_length = 30,required=False)
            

# class UserSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Profile
    #     fields = '__all__'