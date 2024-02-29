from django.shortcuts import render
from rest_framework import APIView,status
from rest_framework.request import Request

class QuizApi(APIView):
    def post(self,request:Request,format=None):
        
        
        return Request(status= status.HTTP_200_OK)
    