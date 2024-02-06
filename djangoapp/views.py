from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile
from .serializers import CreateProfileSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status 

class ProfileApi(APIView):
    def post(self,request:Request,format=None):
        serializer = CreateProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # validated_data = serializer.validated_data
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
            
            
# @api_view(['GET'])
# def getData(request):
#     users = Profile.objects.all()
#     serializer = UserSerializer(users,many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getUser(request,pk):
#     user = Profile.objects.get(id = pk)
#     serializer = UserSerializer(user,many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def addUser(request):
#     serializer = UserSerializer(data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
        
#     return Response(serializer.data)

# @api_view(['PUT'])
# def updateUser(request,pk):
#     user = Profile.objects.get(id = pk)
#     serializer = UserSerializer(instance=user,data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()
        
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def deleteUser(request,pk):
#     user = Profile.objects.get(id=pk)
#     user.delete()
#     return Response("User deleted Successfully")            
        