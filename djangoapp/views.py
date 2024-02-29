from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile
from .serializers import CreateProfileSerializer,ProfileSerializer,updateProfileSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User



class ProfileApi(APIView):
    def post(self, request: Request, format=None):
        serializer = CreateProfileSerializer(data=request.data)
        if serializer.is_valid():
            Profile.objects.create(
                user=request.user,
                username=serializer.validated_data['username'],
                name=serializer.validated_data.get('name'),
                email=serializer.validated_data.get('email'),
                phone_number=serializer.validated_data.get('phone_number')
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request:Request,format=None):
        user = request.user
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProfileSerializer(user.profile, context={'request': request})
            return Response(serializer.data,status=status.HTTP_200_OK)    
        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
            
        
    def put(self,request:Request,format=None):
        user = request.user
        
        try:
            profile = get_object_or_404(Profile,user=user)
        except:
            return Response({'error':'User profile not found'},status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(id=user.id)
        serializer = updateProfileSerializer(user.profile,data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            # validated_data = serializer.validated_data
        
        
            
    
            
            
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
        